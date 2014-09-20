


#include "luiBaseElement.h"
#include "luiRoot.h"
#include "luiObject.h"

TypeHandle LUIBaseElement::_type_handle;


NotifyCategoryDef(luiBaseElement, ":lui");

LUIBaseElement::LUIBaseElement(PyObject *self) :   
  _visible(true), 
  _offset_x(0),
  _offset_y(0),
  _pos_x(0),
  _pos_y(0),
  _rel_pos_x(0),
  _rel_pos_y(0),
  _placement_x(M_default),
  _placement_y(M_default),
  _size(0),
  _parent(NULL),
  _root(NULL),
  _local_z_index(0.5),
  _z_index(0.0),
  _events_registered(false),
  _in_update_section(false),
  _snap_position(true),
  LUIColorable()
{

  _margin = new LUIBounds(0,0,0,0);
  _padding = new LUIBounds(0,0,0,0);

  if (self != NULL) {
    // cout << "Got self instance:" << self << endl;

    PyObject *class_dict = Py_TYPE(self)->tp_dict;

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    string event_func_prefix = "on_";

    // Get all attributes
    while (PyDict_Next(class_dict, &pos, &key, &value)) {

      // Check if the attribute / method is a method
      if (PyFunction_Check(value)) {

        // Get method name
        char *str;
        Py_ssize_t len;

        if (PyString_AsStringAndSize(key, &str, &len) == 0) {
          string method_name(str, len);

          if (method_name.substr(0, event_func_prefix.size()) == event_func_prefix) {
            // cout << "Handler: " << method_name << endl;

            // Bind to event
            string event_name = method_name.substr(event_func_prefix.size());
            // cout << "binding to: '" << event_name << "'" << endl; 

            PyObject *bound_method = PyMethod_New(value, self, (PyObject *)Py_TYPE(self));
            bind(event_name, bound_method);
            Py_DECREF(bound_method); 

          }
        }
      }          
    }
  }
}

LUIBaseElement::~LUIBaseElement() {
  _events.clear();
}

void LUIBaseElement::recompute_position() {
  if (_in_update_section) return;

  if (!_visible) {
    // Just move out of the view frustum. Hacky but works fine :)
    _pos_x = 999999.0;
    _pos_y = 999999.0;
    on_bounds_changed();
    return;
  } 

  LVector2 ppos(0);

  // When there is no parent, there is no sense in computing an accurate position
  if (_parent == NULL) {
    _rel_pos_x = _offset_x;
    _rel_pos_x = _offset_y;


  } else {

    // Recompute actual position from top/bottom and left/right offsets
    ppos = _parent->get_abs_pos();
    LVector2 psize = _parent->get_size();
    LUIBounds* ppadding = _parent->get_padding();

    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Compute, bounds = " << psize.get_x() << ", " 
        << psize.get_y() << ", pos = " << ppos.get_x() 
        << ", " << ppos.get_y() << ", place = " << _placement_x << " / " << _placement_y 
        << ", margin = " << _margin->get_top() << ", " << _margin->get_right() << ", " 
        << _margin->get_bottom() << ", " << _margin->get_left() << ", p_padding = " 
        << ppadding->get_top() << ", " << ppadding->get_right() << ", " << ppadding->get_bottom() << ", " << ppadding->get_left()
        << ", size = " << _size.get_x() << " / " << _size.get_y()
        << endl;
    }

    // Compute top
    // Stick top
    if (_placement_y == M_default) {
      _rel_pos_y = _offset_y + _margin->get_top() + ppadding->get_top();

    // Stick bottom
    } else if (_placement_x == M_inverse) {
      _rel_pos_y = psize.get_y() - _offset_y - _size.get_y() - _margin->get_bottom() - ppadding->get_bottom();
    
    // Stick center
    } else {
      _rel_pos_y = (psize.get_y() - _size.get_y()) / 2.0 + 
                   (_margin->get_top() - _margin->get_bottom()) + 
                   (ppadding->get_top() - ppadding->get_bottom());
    }

    // Compute left
    // Stick left
    if (_placement_x == M_default) {
      _rel_pos_x = _offset_x + _margin->get_left() + ppadding->get_left();

    // Stick right
    } else if (_placement_x == M_inverse) {
      _rel_pos_x = psize.get_x() - _offset_x - _size.get_x() - _margin->get_right() - ppadding->get_right();
    
    // Center Element
    } else {
      _rel_pos_x = (psize.get_x() - _size.get_x()) / 2.0 + 
                   (_margin->get_left() - _margin->get_right()) + 
                   (ppadding->get_left() - ppadding->get_right());
    }
  }

  if (_snap_position) {
    _rel_pos_x = ceil(_rel_pos_x);
    _rel_pos_y = ceil(_rel_pos_y);
  }


  _pos_x = _rel_pos_x + ppos.get_x();
  _pos_y = _rel_pos_y + ppos.get_y();

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "new position is " << _rel_pos_x << " / " << _rel_pos_y << " (abs: " << _pos_x << " / " << _pos_y << ")" << endl;
  }

  on_bounds_changed();
}

void LUIBaseElement::register_events() {

  if (_root != NULL && _parent != NULL && !_events_registered && _events.size() > 0) {
      _root->register_event_object(this);
      _events_registered = true;

      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Registering events for object .." << endl;
      }
  } else {
    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Did not register events, root = " << (_root==NULL?"NULL":"valid") << ", registered = " << (_events_registered ? "1":"0") << ", parent = " << (_parent==NULL?"NULL" : "valid") << " .." << endl;
    }
  }
}

void LUIBaseElement::unregister_events() {

  if (_root != NULL && _events_registered) {
    _root->unregister_event_object(this);
    _events_registered = false;
  
    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Un-registering events for object .." << endl;
    }
  } else {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Did not unregister events, root = " << (_root==NULL?"NULL":"valid") << ", registered = " << (_events_registered ? "1":"0") << " .." << endl;
      }
  }
}

void LUIBaseElement::reparent_to(LUIBaseElement *parent) {
  if (_parent != NULL) {

    LUIObject *parent_as_object = DCAST(LUIObject, _parent);

    // If this throws, our current parent is not a LUIObject (How can this ever be possible?)
    nassertv(parent_as_object != NULL);
    parent_as_object->remove_child(this);
  }

  LUIObject *new_parent_as_object = DCAST(LUIObject, parent);

  if (new_parent_as_object == NULL) {
    luiBaseElement_cat.error() << "You can only attach elements to a LUIObject (or a subclass of it)" << endl;
    return;
  }
  
  new_parent_as_object->add_child(this);
}





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

  // We could do _margin() but that gives a warning
  for (int i = 0; i < 4; ++i) {
    _margin[i] = 0.0;
  }

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
    // Just move out of the view frustum. Should be enough
    _pos_x = 999999.0;
    _pos_y = 999999.0;
    on_bounds_changed();
    return;
  } 

  // Recompute actual position from top/bottom and left/right offsets
  LVector2 parent_size(0);
  LVector2 parent_pos(0);

  if (_parent != (LUIBaseElement*)NULL) {
    parent_size = _parent->get_size();
    parent_pos = _parent->get_abs_pos();
  };

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Recomputing, bounds = " << parent_size.get_x() << ", " 
      << parent_size.get_y() << ", pos = " << parent_pos.get_x() 
      << ", " << parent_pos.get_y() << endl;
  }

  _rel_pos_x = compute_left();
  _rel_pos_y = compute_top();

  if (_snap_position) {
    _rel_pos_x = ceil(_rel_pos_x);
    _rel_pos_y = ceil(_rel_pos_y);
  }

  _pos_x = _rel_pos_x + parent_pos.get_x();
  _pos_y = _rel_pos_y + parent_pos.get_y();

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
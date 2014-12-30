


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
  _z_offset(0.0),
  _events_registered(false),
  _in_update_section(false),
  _snap_position(true),
  _focused(false),
  _clip_bounds(NULL),
  _abs_clip_bounds(NULL),
  _last_frame_visible(-1),
  _last_render_index(-1),
  _topmost(false),
  LUIColorable()
{

  _margin = new LUIBounds(0,0,0,0);
  _padding = new LUIBounds(0,0,0,0);
  _abs_clip_bounds = new LUIRect(0,0,1e6,1e6);

  // This code here should belong in a _ext file, but that's currently 
  // not supported by interrogate.

  // This code checks for function named "on_xxx" where xxx is an event
  // name, and auto-registers them, which is equal to bind("on_xxx", handler).
  if (self != NULL) {

    PyObject *class_dict = Py_TYPE(self)->tp_dict;

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    string event_func_prefix = "on_";

    // Get all attributes of the python object
    while (PyDict_Next(class_dict, &pos, &key, &value)) {

      // Check if the attribute is a method
      if (PyFunction_Check(value)) {

        // Get the method name
        char *str;
        Py_ssize_t len;

        if (PyString_AsStringAndSize(key, &str, &len) == 0) {
          string method_name(str, len);

          // Check if the method name starts with the required prefix
          if (method_name.substr(0, event_func_prefix.size()) == event_func_prefix) {
            // Bind to event
            string event_name = method_name.substr(event_func_prefix.size());

            // The method handle we get is unbound, create a bound method which we can
            // call directly
            PyObject *bound_method = PyMethod_New(value, self, (PyObject *)Py_TYPE(self));
            bind(event_name, bound_method);
            // The PythonCallbackObject stores a reference, so we can decrease
            // the reference count.
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

  LVector2 ppos(0);  

    float add_x = 0.0;
    float add_y = 0.0;

  // When there is no parent, there is no sense in computing an accurate position
  if (_parent == NULL) {

    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Compute, parent is none" << endl;
    }
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
        if (_clip_bounds != NULL) {
          luiBaseElement_cat.spam()  << "clip = " << _clip_bounds->get_top() << ", " << _clip_bounds->get_right() << ", " << _clip_bounds->get_bottom() << ", " << _clip_bounds->get_left() << endl;
        }
    }


    // Compute top
    // Stick top
    if (_placement_y == M_default) {
      _rel_pos_y = _offset_y;
      add_y = _margin->get_top() + ppadding->get_top();

    // Stick bottom
    } else if (_placement_y == M_inverse) {
      _rel_pos_y = psize.get_y() - _offset_y - _size.get_y();
      add_y = -_margin->get_bottom() - ppadding->get_bottom();

    // Stick center
    } else {
      _rel_pos_y = (psize.get_y() - _size.get_y()) / 2.0;
      add_y = (_margin->get_top() - _margin->get_bottom()) + 
              (ppadding->get_top() - ppadding->get_bottom());
    }

    // Compute left
    // Stick left
    if (_placement_x == M_default) {
      _rel_pos_x = _offset_x;
      add_x = _margin->get_left() + ppadding->get_left();

    // Stick right
    } else if (_placement_x == M_inverse) {
      _rel_pos_x = psize.get_x() - _offset_x - _size.get_x();
      add_x = - _margin->get_right() - ppadding->get_right();

    // Center Element
    } else {
      _rel_pos_x = (psize.get_x() - _size.get_x()) / 2.0;
       add_x = (_margin->get_left() - _margin->get_right()) + 
                   (ppadding->get_left() - ppadding->get_right());
    }
  }

  if (_snap_position) {
    _rel_pos_x = ceil(_rel_pos_x);
    _rel_pos_y = ceil(_rel_pos_y);
  }


  _pos_x = _rel_pos_x + ppos.get_x() + add_x;
  _pos_y = _rel_pos_y + ppos.get_y() + add_y;

  // Compute clip rect

  // Transform local clip bounds to absolute bounds
  float bx1 = _pos_x;
  float by1 = _pos_y;
  float bx2 = bx1 + _size.get_x();
  float by2 = by1 + _size.get_y();

  if (_clip_bounds != NULL) {
    bx1 += _clip_bounds->get_left();
    by1 += _clip_bounds->get_top();
    bx2 += -_clip_bounds->get_right();
    by2 += -_clip_bounds->get_bottom();
  }

  bool ignoreParentBounds = _topmost && !_parent->is_topmost();

  if (_parent != NULL && !ignoreParentBounds) {
    LUIRect *parent_bounds = _parent->get_abs_clip_bounds();

    // If we have no specific bounds, just take the parent bounds
    if (_clip_bounds == NULL) {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Using parent bounds (" << _parent << ") (no custom) (" << parent_bounds->get_x() << ", " 
          << parent_bounds->get_y() << " / " << parent_bounds->get_w() << " x " << parent_bounds->get_h() << ") .." << endl;
      }
      _abs_clip_bounds->set_rect(parent_bounds->get_rect());
    } else {

      // Intersect parent bounds with local bounds
      float nx = max(bx1, parent_bounds->get_x());
      float ny = max(by1, parent_bounds->get_y());
      float nw = max(0.0f, min(bx2, parent_bounds->get_x() + parent_bounds->get_w()) - nx);
      float nh = max(0.0f, min(by2, parent_bounds->get_y() + parent_bounds->get_h()) - ny);

      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Using merged bounds (parent+custom) " << endl;
      }
      _abs_clip_bounds->set_rect(nx, ny, nw, nh);
    }

  } else {

    if (_clip_bounds == NULL) {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Using no bounds .." << endl;
      }
      _abs_clip_bounds->set_rect(0,0,1000000,1000000);
    } else {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Using local bounds (custom) .." << endl;
      }
      _abs_clip_bounds->set_rect(bx1, by1, max(0.0f, bx2 - bx1), max(0.0f, by2 - by1));
    }
  }

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "new position is " << _rel_pos_x << " / " << _rel_pos_y << " (abs: " << _pos_x << " / " << _pos_y << "), bounds=(" 
      << _abs_clip_bounds->get_x() << ", " << _abs_clip_bounds->get_y() << ", " << _abs_clip_bounds->get_w() << " x " << _abs_clip_bounds->get_h() << ")" << endl;

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

    // If this throws, our current parent is not a LUIObject, or a base class of it (How can this ever be possible?)
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


void LUIBaseElement::request_focus() {
  _root->request_focus(this);
}


void LUIBaseElement::blur() {
  _root->request_focus(NULL);
}

void LUIBaseElement::fetch_render_index() {
  if (_root == NULL) {
    _last_render_index = -1;
  } else {
    _last_render_index = _root->allocate_render_index();
  } 
}
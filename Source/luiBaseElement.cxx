
#include "luiBaseElement.h"

#include "luiRoot.h"
#include "luiObject.h"
#include "luiEventData.h"
#include "pythonCallbackObject.h"

// Temporary
#include "py_panda.h"

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
  _last_frame_visible(-1),
  _last_render_index(-1),
  _topmost(false),
  _solid(false),
  _emits_changed_event(true),
  _last_bounds(),
  _last_clip_bounds(),
  _margin(0, 0, 0, 0),
  _padding(0, 0, 0, 0),
  _abs_clip_bounds(0, 0, 1e6, 1e6),
  _clip_bounds(0, 0, 0, 0),
  _have_clip_bounds(false),
  LUIColorable()
{
  // This code here should belong in a _ext file, but that's currently
  // not supported by interrogate.

  // This code checks for function named "on_xxx" where xxx is an event
  // name, and auto-registers them, which is equal to bind("on_xxx", handler).
  if (self != NULL) {

    PyObject *class_methods = PyObject_Dir((PyObject *)Py_TYPE(self));
    nassertv(class_methods != NULL);
    nassertv(PyList_Check(class_methods));

    Py_ssize_t num_elements = PyList_Size(class_methods);
    Py_ssize_t pos = 0;

    string event_func_prefix = "on_";

    // bind() no longer takes a PyObject* directly, so we have to do this.
    // We have to pre-initialize self before we can call bind, though, since
    // interrogate can't do this until after the constructor is called.
    ((Dtool_PyInstDef *)self)->_ptr_to_object = (void *)this;
    PyObject *bind_func = PyObject_GetAttrString(self, "bind");
    nassertv(bind_func != NULL);

    // Get all attributes of the python object
    for (Py_ssize_t i = 0; i < num_elements; ++i) {

      PyObject* method_name = PyList_GetItem(class_methods, i);

      char *str;
      Py_ssize_t len;

      // Get the method name as string
      if (PyString_AsStringAndSize(method_name, &str, &len) == 0) {
        string method_name_str(str, len);

        // Check if the method name starts with the required prefix
        if (method_name_str.substr(0, event_func_prefix.size()) == event_func_prefix) {

          PyObject* method = PyObject_GenericGetAttr(self, method_name);
          nassertv(method != NULL);

          // Check if the attribute is a method
          if (PyCallable_Check(method)) {
              // Bind to event
              PyObject_CallFunction(bind_func, (char *)"s#O",
                str + event_func_prefix.size(), len - event_func_prefix.size(), method);
          }
        }
      }
    }

    Py_DECREF(class_methods);
  }
}

LUIBaseElement::~LUIBaseElement() {
}

void LUIBaseElement::recompute_position() {
  if (_in_update_section) return;

  /*


   TODO: Use pandas builtin vector types to make this computations prettier


  */

  LVector2 ppos(0);

  float add_x = 0.0;
  float add_y = 0.0;

  if (!_parent) {
    // When there is no parent, there is no sense in computing an accurate position
    _rel_pos_x = _offset_x;
    _rel_pos_y = _offset_y;

  } else {

    // Recompute actual position from top/bottom and left/right offsets
    ppos = _parent->get_abs_pos();
    LVector2 psize = _parent->get_size();
    const LUIBounds& ppadding = _parent->get_padding();

    // Compute top
    // Stick top
    if (_placement_y == M_default) {
      _rel_pos_y = _offset_y;
      add_y = _margin.get_top() + ppadding.get_top();

    // Stick bottom
    } else if (_placement_y == M_inverse) {
      _rel_pos_y = psize.get_y() - _offset_y - _size.get_y();
      add_y = -_margin.get_bottom() - ppadding.get_bottom();

    // Stick center
    } else {
      _rel_pos_y = (psize.get_y() - _size.get_y()) / 2.0;
      add_y = (_margin.get_top() - _margin.get_bottom()) +
              (ppadding.get_top() - ppadding.get_bottom());
    }

    // Compute left
    // Stick left
    if (_placement_x == M_default) {
      _rel_pos_x = _offset_x;
      add_x = _margin.get_left() + ppadding.get_left();

    // Stick right
    } else if (_placement_x == M_inverse) {
      _rel_pos_x = psize.get_x() - _offset_x - _size.get_x();
      add_x = - _margin.get_right() - ppadding.get_right();

    // Center Element
    } else {
      _rel_pos_x = (psize.get_x() - _size.get_x()) / 2.0;
       add_x = (_margin.get_left() - _margin.get_right()) +
               (ppadding.get_left() - ppadding.get_right());
    }
  }

  // In case we snap our position (Default, except for text sprites), we just ceil
  // our position. This prevents subpixel-jittering.
  if (_snap_position) {
    _rel_pos_x = ceil(_rel_pos_x);
    _rel_pos_y = ceil(_rel_pos_y);
  }

  _pos_x = _rel_pos_x + ppos.get_x() + add_x;
  _pos_y = _rel_pos_y + ppos.get_y() + add_y;

  // Compute clip rect:
  // Transform local clip bounds to absolute bounds
  float bx1 = _pos_x;
  float by1 = _pos_y;
  float bx2 = bx1 + _size.get_x();
  float by2 = by1 + _size.get_y();

  if (_have_clip_bounds) {
    bx1 += _clip_bounds.get_left();
    by1 += _clip_bounds.get_top();
    bx2 += -_clip_bounds.get_right();
    by2 += -_clip_bounds.get_bottom();
  }

  bool ignore_parent_bounds = _topmost && !_parent->is_topmost();

  if (_parent && !ignore_parent_bounds) {
    const LUIRect& parent_bounds = _parent->get_abs_clip_bounds();

    // If we have no specific bounds, just take the parent bounds
    if (!_have_clip_bounds) {
      _abs_clip_bounds = parent_bounds;
    } else {
      // Intersect parent bounds with local bounds
      float nx = max(bx1, parent_bounds.get_x());
      float ny = max(by1, parent_bounds.get_y());
      float nw = max(0.0f, min(bx2, parent_bounds.get_x() + parent_bounds.get_w()) - nx);
      float nh = max(0.0f, min(by2, parent_bounds.get_y() + parent_bounds.get_h()) - ny);
      _abs_clip_bounds.set_rect(nx, ny, nw, nh);
    }

  } else {
    if (!_have_clip_bounds) {
      // In case we have no clip bounds, set some arbitrary huge bounds
      _abs_clip_bounds.set_rect(0, 0, 1e6, 1e6);
    } else {
      _abs_clip_bounds.set_rect(bx1, by1, max(0.0f, bx2 - bx1), max(0.0f, by2 - by1));
    }
  }

  LUIRect current_bounds(_pos_x, _pos_y, _size.get_x(), _size.get_y());

  if (current_bounds != _last_bounds || _abs_clip_bounds != _last_clip_bounds) {
    _last_bounds = current_bounds;
    _last_clip_bounds = _abs_clip_bounds;
    on_bounds_changed();
  } else {
  }

}

void LUIBaseElement::register_events() {
  if (_root && _parent && !_events_registered && _solid) {
      _root->register_event_object(this);
      _events_registered = true;

      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Registering events for object .." << endl;
      }
  } else {
    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Did not register events, root = " << (_root==NULL?"NULL":"valid")
                                << ", registered = " << (_events_registered ? "1":"0") << ", parent = "
                                << (_parent==NULL?"NULL" : "valid") << " .." << endl;
    }
  }
}

void LUIBaseElement::unregister_events() {
  if (_root && _events_registered) {
    _root->unregister_event_object(this);
    _events_registered = false;

    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Un-registering events for object .." << endl;
    }
  } else {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Did not unregister events, root = " << (_root == NULL?"NULL":"valid")
                                  << ", registered = " << (_events_registered ? "1":"0") << " .." << endl;
      }
  }
}

void LUIBaseElement::set_parent(LUIObject* parent) {
  // Detach from current parent
  if (_parent)
    _parent->remove_child(this);

  // Attach to new parent
  parent->add_child(this);
}

void LUIBaseElement::request_focus() {
  if (_root->request_focus(this))
    _focused = true;
}

void LUIBaseElement::blur() {
  _root->request_focus(NULL);

  // Giving away focus will always work, so we can already set our focus state
  _focused = false;
}

void LUIBaseElement::fetch_render_index() {
  if (_root == NULL) {
    _last_render_index = -1;
  } else {
    _last_render_index = _root->allocate_render_index();
  }
}

void LUIBaseElement::trigger_event(const string &event_name, const wstring &message, const LPoint2 &coords) {
  auto elem_it = _events.find(event_name);
  if (elem_it != _events.end()) {
      PT(LUIEventData) data = new LUIEventData(this, event_name, message, coords);
      elem_it->second->do_callback(data);
  }
}

void LUIBaseElement::set_z_offset(int z_offset) {
  _z_offset = (float)z_offset;

  // Notify parent about changed z-index - so the children can be re-sorted
  if (_parent)
    _parent->on_child_z_offset_changed();
}


float LUIBaseElement::get_parent_width() const {
  if (!_parent)
    return 0.0;
  return _parent->get_width();
}

float LUIBaseElement::get_parent_height() const {
  if (!_parent)
    return 0.0;
  return _parent->get_height();
}

void LUIBaseElement::on_color_changed() {
  if (_parent) {
    compose_color(_parent->get_composed_color());
  } else {
    compose_color();
  }
}

void LUIBaseElement::clear_parent() {
  if (!_parent) {
    luiBaseElement_cat.error() << "Called clear_parent(), but no parent is set!" << endl;
    return;
  }
  _parent->remove_child(this);
}

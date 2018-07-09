
#include "luiBaseElement.h"

#include "luiRoot.h"
#include "luiObject.h"
#include "luiEventData.h"
#include "pythonCallbackObject.h"

// Temporary
#include "py_panda.h"

TypeHandle LUIBaseElement::_type_handle;
NotifyCategoryDef(luiBaseElement, ":lui");

/**
 * @brief Constructs a new LUIBaseElement
 * @details This constructs a new LUIBaseElement, initializing all properties.
 *   The self pointer should be usually nullptr. For python objects, interrogate
 *   automatically passes a handle to the object as the self pointer.
 *   When a self pointer is passed, all methods named on_xxx are automatically
 *   bound to events using LUIBaseElement::bind().
 *
 * @param self self-pointer or null
 */
LUIBaseElement::LUIBaseElement(PyObject* self) :
  _position(0.0f),
  _abs_position(0.0f),
  _effective_size(0.0f),
  _visible(true),
  _z_offset(0.0f),
  _events_registered(false),
  _snap_position(true),
  _focused(false),
  _solid(false),
  _margin(0.0f),
  _padding(0.0f),
  _clip_bounds(0.0f, 0.0f, 1e6, 1e6),
  _have_clip_bounds(false),
  _abs_clip_bounds(0.0f, 0.0f, 1e6, 1e6),
  _parent(nullptr),
  _root(nullptr),
  _last_frame_visible(-1),
  _last_render_index(-1),
  _topmost(false),
  _debug_name("LUIBaseElement"),
  _name(""),
  LUIColorable()
{
 load_python_events(self);
}

LUIBaseElement::~LUIBaseElement() {
}

/**
 * @brief Loads all events from a python object
 * @details This registers all methods which are named on_xxx as events using
 *   LUIBaseElement::bind(). This prevents the user from having to call bind
 *   for every event method.
 *
 * @param self Python object self-pointer, or null
 */
void LUIBaseElement::load_python_events(PyObject* self) {
  // This code here should belong in a _ext file, but that's currently
  // not supported by interrogate.

  // This code checks for function named "on_xxx" where xxx is an event
  // name, and auto-registers them, which is equal to bind("on_xxx", handler).
  if (self != nullptr) {

    PyObject* class_methods = PyObject_Dir((PyObject*)Py_TYPE(self));
    nassertv(class_methods != nullptr);
    nassertv(PyList_Check(class_methods));

    Py_ssize_t num_elements = PyList_Size(class_methods);
    Py_ssize_t pos = 0;

    string event_func_prefix = "on_";

    // bind() no longer takes a PyObject* directly, so we have to do this.
    // We have to pre-initialize self before we can call bind, though, since
    // interrogate can't do this until after the constructor is called.
    ((Dtool_PyInstDef *)self)->_ptr_to_object = (void *)this;
    PyObject *bind_func = PyObject_GetAttrString(self, "bind");
    nassertv(bind_func != nullptr);

    // Get all attributes of the python object
    for (Py_ssize_t i = 0; i < num_elements; ++i) {

      PyObject* method_name = PyList_GetItem(class_methods, i);
#if PY_MAJOR_VERSION >= 3
      const
#endif
      char* str;
      Py_ssize_t len;

      // Get the method name as string
#if PY_MAJOR_VERSION >= 3
      str = PyUnicode_AsUTF8AndSize(method_name, &len ); 
      if ( str ) {
#else
      if (PyString_AsStringAndSize(method_name, &str, &len) == 0) {
#endif
        string method_name_str(str, len);

        // Check if the method name starts with the required prefix
        if (method_name_str.substr(0, event_func_prefix.size()) == event_func_prefix) {

          PyObject* method = PyObject_GenericGetAttr(self, method_name);
          nassertv(method != nullptr);

          // Check if the attribute is a method
          if (PyCallable_Check(method)) {
              // Bind to event
              PyObject_CallFunction(bind_func, (char *)"s#O",
                str + event_func_prefix.size(), len - event_func_prefix.size(), method);
          }

          Py_DECREF(method);
        }
      }
    }

    Py_DECREF(class_methods);
    Py_DECREF(bind_func);

    // Find out the class name on custom python objects
    PyObject* cls = (PyObject*)Py_TYPE(self);
    PyObject* cls_name = PyObject_GetAttrString(cls, "__name__");

#if PY_MAJOR_VERSION >= 3
      const
#endif
    char* str;
    Py_ssize_t len;

    // Get the method name as string
#if PY_MAJOR_VERSION >= 3
    str = PyUnicode_AsUTF8AndSize(cls_name, &len);
    if (str) {
#else
    if (PyString_AsStringAndSize(cls_name, &str, &len) == 0) {
#endif
      _debug_name = string(str, len);
    } else {
      luiBaseElement_cat.warning() << "Failed to extract class name" << endl;
    }

    Py_DECREF(cls_name);

    _debug_name;
  }
}


// Helper function for componentwise vector maximum
INLINE LVector2 componentwise_max(const LVector2& a, const LVector2& b) {
  return LVector2(
    max(a.get_x(), b.get_x()),
    max(a.get_y(), b.get_y())
  );
}

// Helper function for componentwise vector minimum
INLINE LVector2 componentwise_min(const LVector2& a, const LVector2& b) {
  return LVector2(
    min(a.get_x(), b.get_x()),
    min(a.get_y(), b.get_y())
  );
}

/**
 * @brief Internal method to register all events to the LUIRoot
 * @details This method registers the element to the root element, which makes
 *   the element recieve events. This method gets called whenever the object
 *   recieves a new root, or gets parented to a new object.
 */
void LUIBaseElement::register_events() {
  if (_root && _parent && !_events_registered && _solid) {
      _root->register_event_object(this);
      _events_registered = true;

      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Registered events for object" << endl;
      }
  }
}

/**
 * @brief Internal method to unregister all events from the current LUIRoot
 * @details This unregisters the element from the current LUIRoot, making it
 *   no longer recieve any events. This gets called when the element got detached.
 */
void LUIBaseElement::unregister_events() {
  if (_root && _events_registered) {
    _root->unregister_event_object(this);
    _events_registered = false;

    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Un-registered events for object" << endl;
    }
  }
}

/**
 * @brief Sets the elements parent
 * @details This sets the parent of the element. This is equal to calling
 *   parent.add_child(self). If the element currently has a parent, the element
 *   is first removed from the old parent.
 *
 * @param parent New parent of the element.
 */
void LUIBaseElement::set_parent(LUIObject* parent) {
  // Detach from current parent
  if (_parent)
    _parent->remove_child(this);

  // Attach to new parent
  parent->add_child(this);
}

/**
 * @brief Attempts to request focus
 * @details This tries to request focus for the current element. If the element
 *   recieved focus successfully, true is returned, false otherwise.
 * @return Whether the element is focused
 */
bool LUIBaseElement::request_focus() {
  if (_root->request_focus(this))
    _focused = true;
  return _focused;
}

/**
 * @brief Gives focus away
 * @details This makes the element no longer focused. This always succeeds.
 */
void LUIBaseElement::blur() {
  if (!_focused)
    luiBaseElement_cat.warning() << "Called blur(), but element was not focused, target = "
                                 << _debug_name << endl;

  _root->request_explicit_blur();

  // Giving away focus will always work, so we can already set our focus state
  _focused = false;
}

/**
 * @brief Internal method to get the rendered index
 * @details This method asks the LUIRoot for the render index counter, and stores
 *   it as the last render index.
 */
void LUIBaseElement::fetch_render_index() {
  if (_root == nullptr) {
    _last_render_index = -1;
  } else {
    _last_render_index = _root->allocate_render_index();
  }
}

/**
 * @brief Triggers an event
 * @details This triggers an event with the given name and a message. Optionally
 *   coordinates can be passed, e.g. for mousemove events.
 *   If no event handler is bound to this event, nothing happens. Otherwise the
 *   event handler is called with the event data.
 *
 * @param event_name Name of the event
 * @param message Optional message of the event
 * @param coords Optional coordinates of the event
 */
void LUIBaseElement::trigger_event(const string& event_name, const wstring& message, const LPoint2& coords) {
  trigger_event(new LUIEventData(this, event_name, message, coords));
}

/**
 * @brief Triggers an event
 * @details This triggers an event with the given EventData.
 *   If no event handler is bound to this event, nothing happens. Otherwise the
 *   event handler is called with the event data.
 *
 * @param data Event data
 */
void LUIBaseElement::trigger_event(PT(LUIEventData) data) {
  auto elem_it = _events.find(data->get_name());
  if (elem_it != _events.end()) {
      elem_it->second->do_callback(data);
  }
}

void LUIBaseElement::set_z_offset(float z_offset) {
  _z_offset = z_offset;

  // Notify parent about changed z-index - so the children can be re-sorted
  if (_parent)
    _parent->on_child_z_offset_changed();
}

float LUIBaseElement::get_parent_width() const {
  if (!_parent)
    return 0.0f;
  return _parent->get_width();
}

float LUIBaseElement::get_parent_height() const {
  if (!_parent)
    return 0.0f;
  return _parent->get_height();
}

void LUIBaseElement::clear_parent() {
  if (!_parent) {
    luiBaseElement_cat.error() << "Called clear_parent(), but no parent is set! target = " << _debug_name << endl;
    return;
  }
  _parent->remove_child(this);
}

LVector2 LUIBaseElement::get_available_dimensions() const {
  if (!_parent)
    return LVector2(0);

  const LUIBounds& parent_padding = _parent->_padding;
  const LVector2& parent_size = _parent->_effective_size;

  // Compute how much pixels 100% would be, this is required for relative widths
  // and heights like 23%. We start at the full size:
  LVector2 available_dimensions = parent_size;

  // Due to the parents padding, there is also less space available
  available_dimensions.add_x(- (parent_padding.get_left() + parent_padding.get_right()));
  available_dimensions.add_y(- (parent_padding.get_top() + parent_padding.get_bottom()));

  // If the current element has margin, then that also reduces the available space
  available_dimensions.add_x(- (_margin.get_left() + _margin.get_right()));
  available_dimensions.add_y(- (_margin.get_top() + _margin.get_bottom()));

  return available_dimensions;
}

void LUIBaseElement::update_dimensions() {
  if (!_size.x.has_expression()) {
    luiBaseElement_cat.warning() << "LUIBaseElement has no valid width expression! target = " << _debug_name << endl;
  }

  if (!_size.y.has_expression()) {
    luiBaseElement_cat.warning() << "LUIBaseElement has no valid height expression! target = " << _debug_name << endl;
  }

  LVector2 available_dimensions = get_available_dimensions();
  _effective_size.set(
    _size.x.evaluate(available_dimensions.get_x()),
    _size.y.evaluate(available_dimensions.get_y())
  );
}

void LUIBaseElement::update_dimensions_upstream() {
  update_dimensions();
}

void LUIBaseElement::update_position() {

  const LVector2& parent_size = _parent->_effective_size;
  const LPoint2& parent_pos = _parent->_abs_position;
  const LUIBounds& parent_padding = _parent->_padding;

  if (_placement.x == M_default) {
    _abs_position.set_x( _margin.get_left() + parent_padding.get_left() + parent_pos.get_x() + _position.get_x() );
  } else if (_placement.x == M_inverse) {
    _abs_position.set_x(parent_pos.get_x() + parent_size.get_x() - _position.get_x()
                        - _effective_size.get_x() - _margin.get_right() - parent_padding.get_right());
  } else if (_placement.x == M_center) {
    _abs_position.set_x(
      parent_pos.get_x() + (parent_size.get_x() - _effective_size.get_x()) / 2.0f
      + _margin.get_left() - _margin.get_right() + parent_padding.get_left() - parent_padding.get_right()
    );
  }

  // Compute the y-position, same as for the x-position
  if (_placement.y == M_default) {
    _abs_position.set_y( _margin.get_top() + parent_padding.get_top() + parent_pos.get_y() + _position.get_y() );
  } else if (_placement.y == M_inverse) {
    _abs_position.set_y(parent_pos.get_y() + parent_size.get_y() - _position.get_y()
                        - _effective_size.get_y() - _margin.get_bottom() - parent_padding.get_bottom());
  } else if (_placement.y == M_center) {
    _abs_position.set_y(
      parent_pos.get_y() + (parent_size.get_y() - _effective_size.get_y()) / 2.0f
      + _margin.get_top() - _margin.get_bottom() + parent_padding.get_top() - parent_padding.get_bottom()
    );
  }
}

void LUIBaseElement::update_downstream() {

  // Reset temporary attributes
  // _abs_position.set(0, 0);
  // _effective_size.set(0, 0);

  // In the downstream pass, following attributes are updated:
  // - absolute position for elements which are aligned top / right
  // - width/height

  if (_parent) {
    update_position();
    update_dimensions();

    // Update the color
    compose_color(_parent->get_composed_color());
  } else {

    // When we have no parent, we are the root, so we don't need a good position.
    // (Stuff like margin and padding is not supported on the root element)
    _abs_position = _position;
    _effective_size = LVector2(_size.x.evaluate(0), _size.y.evaluate(0));
    _abs_clip_bounds.set_rect(0, 0, 1e6, 1e6);
    compose_color(LColor(1));
  }

  // After computing everything, snap the position if specified
  if (_snap_position) {
    _effective_size.set_x(ceil(_effective_size.get_x()));
    _effective_size.set_y(ceil(_effective_size.get_y()));
    _abs_position.set_x(ceil(_abs_position.get_x()));
    _abs_position.set_y(ceil(_abs_position.get_y()));
    // TODO: Clamp absolute clip bounds
  }

}

void LUIBaseElement::update_upstream() {

  // In the upstream pass, the following attributes are updated:
  // - absolute position for elements which are aligned right / bottom
  // - width/height for elements without explicit size
  if (_parent) {
    update_position();
    update_dimensions();
  } else {
    // In case of no parent, we are the root element. In that case, we don't really
    // have to do anything.
  }
}


void LUIBaseElement::update_clip_bounds() {

  // In case we have no parent, we don't need bounds
  if (!_parent)
    return;

  // Compute clip rect:
  // Transform local clip bounds to absolute bounds
  LVector2 abs_bounds_start(_abs_position);
  LVector2 abs_bounds_end(_abs_position + _effective_size);

  // Add local clip bounds
  if (_have_clip_bounds) {
    abs_bounds_start.add_x(_clip_bounds.get_left());
    abs_bounds_start.add_y(_clip_bounds.get_top());
    abs_bounds_end.add_x(-_clip_bounds.get_right());
    abs_bounds_end.add_y(-_clip_bounds.get_bottom());
  }

  // Topmost elements skip clip bounds of their parents
  bool ignore_parent_bounds = _topmost && !_parent->is_topmost();

  if (!ignore_parent_bounds) {
    const LUIRect& parent_bounds = _parent->_abs_clip_bounds;

    if (!_have_clip_bounds) {
      // If we have no specific bounds, just take the parent bounds
      _abs_clip_bounds = parent_bounds;
    } else {
      // Intersect parent bounds with local bounds
      // abs_bounds_start = componentwise_max(abs_bounds_start, parent_bounds.get_xy());
      abs_bounds_end = componentwise_min(abs_bounds_end, parent_bounds.get_xy() + parent_bounds.get_wh());
      abs_bounds_end = componentwise_max(abs_bounds_end, LVector2(0)); // Make sure we don't have negative bounds
      _abs_clip_bounds.set_rect(abs_bounds_start, abs_bounds_end - abs_bounds_start);
    }

  } else {
    if (!_have_clip_bounds) {
      // In case we have no clip bounds, set some arbitrary huge bounds
      _abs_clip_bounds.set_rect(0, 0, 1e6, 1e6);
    } else {
      LVector2 local_size = componentwise_max(LVector2(0), abs_bounds_end - abs_bounds_start);
      _abs_clip_bounds.set_rect(abs_bounds_start, local_size);
    }
  }

}

void LUIBaseElement::move_by(const LVector2& offset) {
  _abs_position.add_x(offset.get_x());
  _abs_position.add_y(offset.get_y());
}

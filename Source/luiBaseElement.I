


INLINE void LUIBaseElement::set_top_left(float x, float y) {
  _stick_top = true;
  _stick_left = true;
  _offset_x = x;
  _offset_y = y;
  recompute_position();

}

INLINE void LUIBaseElement::set_pos(float top, float left) {
  set_top_left(top, left);
}

INLINE void LUIBaseElement::set_top(float top) {
  _stick_top = true;
  _offset_y = top;
  recompute_position();
}

INLINE void LUIBaseElement::set_bottom(float bottom) {
  if (_parent == NULL) {
    luiBaseElement_cat.warning() << "Attempting to do set_bottom, but no parent is set yet. " << endl;
  } else if (!_parent->has_size()) {
    luiBaseElement_cat.warning() << "Attempting to do set_bottom, but parent has no size set!" << endl;
  }

  _stick_top = false;
  _offset_y = bottom;
  recompute_position();
}

INLINE void LUIBaseElement::set_left(float left) {
  _stick_left = true;
  _offset_x = left;
  recompute_position();
}

INLINE void LUIBaseElement::set_right(float right) {
  if (_parent == NULL) {
    luiBaseElement_cat.warning() << "Attempting to do set_right, but no parent is set yet. " << endl;
  } else if (!_parent->has_size()) {
    luiBaseElement_cat.warning() << "Attempting to do set_right, but parent has no size set!" << endl;
  }

  _stick_left = false;
  _offset_x = right;
  recompute_position();
}

INLINE LVector2 LUIBaseElement::get_abs_pos() {
  return LVector2(_pos_x, _pos_y);
}

INLINE float LUIBaseElement::get_top() {
  return _pos_y;
}

INLINE float LUIBaseElement::get_left() {
  return _pos_x;
}

INLINE void LUIBaseElement::set_visible(bool visible) {
  _visible = visible;
  on_visibility_changed();
}

INLINE bool LUIBaseElement::is_visible() {
  return _visible;
}

INLINE void LUIBaseElement::hide() {
  set_visible(false);
}

INLINE void LUIBaseElement::show() {
  set_visible(true);
}

INLINE void LUIBaseElement::set_size(const LVector2 &size) {
  set_size(size.get_x(), size.get_y());
}

INLINE void LUIBaseElement::set_size(float w, float h) {
  _size.set_x(w);
  _size.set_y(h);
  recompute_position();
}

INLINE bool LUIBaseElement::has_size() {
  return _size.get_x() != 0.0 && _size.get_y() != 0.0;
}

INLINE void LUIBaseElement::set_width(float w) {
  _size.set_x(w);
  recompute_position();
}

INLINE void LUIBaseElement::set_height(float h) {
  _size.set_y(h);
  recompute_position();
}

INLINE float LUIBaseElement::get_width() {
  return _size.get_x();
}

INLINE float LUIBaseElement::get_height() {
  return _size.get_y(); 
}

INLINE const LVector2 &LUIBaseElement::get_size() const {
  return _size;
}

INLINE void LUIBaseElement::set_parent(LUIBaseElement* parent) {
  _parent = parent;
}

INLINE LUIBaseElement* LUIBaseElement::get_parent() {
  return _parent;
}

INLINE void LUIBaseElement::set_relative_z_index(int z_index) {
  _local_z_index = (float)z_index;
  recompute_z_index();
}

INLINE float LUIBaseElement::get_relative_z_index() {
  return _local_z_index;
}

INLINE float LUIBaseElement::get_absolute_z_index() {
  return _z_index;
}


INLINE void LUIBaseElement::recompute_z_index() {
  if (_parent != NULL) {
    _z_index = _parent->get_absolute_z_index() + _local_z_index;
    nassertv(_z_index > -10000.0 && _z_index < 10000.0);
  } else {
    _z_index = _local_z_index;
  }
  on_z_index_changed();
}


INLINE bool LUIBaseElement::has_event(LUIEvent name) {
  return true;
}

INLINE void LUIBaseElement::trigger_event(LUIEvent name) {
  luiBaseElement_cat.spam() << "Triggering event .." << endl; 
}

INLINE void LUIBaseElement::register_events() {



  if (_root != NULL && _parent != NULL && !_events_registered) {
    // _root->register_event_object(this);
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

INLINE void LUIBaseElement::unregister_events() {

  if (_root != NULL && _events_registered) {
    // _root->unregister_event_object(this);
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

INLINE void LUIBaseElement::begin_update_section() {
  nassertv(_in_update_section == false);
  _in_update_section = true;

  if (lui_cat.spam()) {
    lui_cat.spam() << "Begin of update section .." << endl;
  }
}

INLINE void LUIBaseElement::end_update_section() {
  nassertv(_in_update_section == true);
  _in_update_section = false;  

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "End of update section .." << endl;
  }
  recompute_position();

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Finally left update section .." << endl;
  }
}
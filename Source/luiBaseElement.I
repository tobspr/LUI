


INLINE void LUIBaseElement::bind(const string &event_name, CallbackObject* callback) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << _debug_name << "Binding event '" << event_name << "'" << endl;
  }
  if (_events.count(event_name) != 0) {
    lui_cat.warning() << "Overriding event handler for '" << event_name << "'" << endl;
  }

  _events[event_name] = callback;

  register_events();
}

INLINE void LUIBaseElement::bind(const string &event_name, PyObject* callback) {
  bind(event_name, new PythonCallbackObject(callback));
}

INLINE void LUIBaseElement::unbind(const string &event_name) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << _debug_name << "Unbinding event '" << event_name << "'" << endl;
  }

  if (has_event(event_name)) {
    _events.erase(event_name);
  }

  if (_events.size() < 1) {
    unregister_events();
  }

}

INLINE void LUIBaseElement::unbind_all() {
  _events.clear();
  unregister_events();
}

INLINE bool LUIBaseElement::has_event(const string &event_name) {
  return _events.count(event_name) > 0;
}


INLINE void LUIBaseElement::trigger_event(const string &event_name, const wstring &message, const LPoint2 &coords) {
  // if (luiBaseElement_cat.is_spam()) {
    // luiBaseElement_cat.spam() << _debug_name << "Triggering event '" << event_name << "' with coordinates " 
    // << coords.get_x() << ", " << coords.get_y() << " and message '" << message << "'.." << endl;
  // }

  if (has_event(event_name)) {
      PT(LUIEventData) data = new LUIEventData(this, event_name, message, coords);
      _events[event_name]->do_callback(data);
  }
}

INLINE void LUIBaseElement::set_snap_position(bool snap) {
  _snap_position = snap;
}

INLINE void LUIBaseElement::set_left_top(const LPoint2 &pos) {
  _placement_x = M_default;
  _placement_y = M_default;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_right_top(const LPoint2 &pos) {
  _placement_x = M_inverse;
  _placement_y = M_default;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_left_bottom(const LPoint2 &pos) {
  _placement_x = M_default;
  _placement_y = M_inverse;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_right_bottom(const LPoint2 &pos) {
  _placement_x = M_inverse;
  _placement_y = M_default;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE LPoint2 LUIBaseElement::get_left_top() {
  return LPoint2(get_left(), get_top());
}

INLINE LPoint2 LUIBaseElement::get_right_top() {
  return LPoint2(get_right(), get_top());
}

INLINE LPoint2 LUIBaseElement::get_left_bottom() {
  return LPoint2(get_left(), get_bottom());
}

INLINE LPoint2 LUIBaseElement::get_right_bottom() {
  return LPoint2(get_right(), get_bottom());
}

INLINE void LUIBaseElement::set_pos(const LPoint2 &pos) {
  set_pos(pos.get_x(), pos.get_y());
}

INLINE void LUIBaseElement::set_pos(float x, float y) {
  set_left_top(LPoint2(x, y));
}

INLINE LPoint2 LUIBaseElement::get_pos() {
  return get_left_top();
}

INLINE LPoint2 LUIBaseElement::get_abs_pos() {
  return LPoint2(_pos_x, _pos_y);
}

INLINE void LUIBaseElement::set_top(float top) {
  _placement_y = M_default;
  _offset_y = top;
  recompute_position();
}

INLINE void LUIBaseElement::set_right(float right) {
  _placement_x = M_inverse;
  _offset_x = right;
  recompute_position();
}

INLINE void LUIBaseElement::set_bottom(float bottom) {
  _placement_y = M_inverse;
  _offset_y = bottom;
  recompute_position();
}

INLINE void LUIBaseElement::set_left(float left) {
  _placement_x = M_default;
  _offset_x = left;
  recompute_position();
}

INLINE float LUIBaseElement::get_top() {
  return _rel_pos_y;
}

INLINE float LUIBaseElement::get_right() {
  return get_parent_width() - get_left();
}

INLINE float LUIBaseElement::get_bottom() {
  return get_parent_height() - get_top();
}

INLINE float LUIBaseElement::get_left() {
  return _rel_pos_x;
}

INLINE LPoint2 LUIBaseElement::get_relative_pos(const LPoint2 &abs_pos) {
  return abs_pos - get_abs_pos();
}

INLINE void LUIBaseElement::set_centered(bool center_vert, bool center_horiz) {
  if (center_horiz) {
    _placement_x = M_center;
    _offset_x = 0;
  }
  if (center_vert) {
  _placement_y = M_center;
  _offset_y = 0;
  }

  if (center_vert || center_horiz) {
    recompute_position();
  }
}
INLINE void LUIBaseElement::set_center_vertical(bool centered) {
  if (centered) {
    _placement_y = M_center;
    _offset_y = 0;
    recompute_position();
  }
}

INLINE void LUIBaseElement::set_center_horizontal(bool centered) {
  if (centered) {
    _placement_x = M_center;
    _offset_x = 0;
    recompute_position();
  }
}

INLINE bool LUIBaseElement::is_centered() {
  return _placement_x == M_center && _placement_y == M_center;
}

INLINE bool LUIBaseElement::is_vertical_centered() {
  return _placement_y == M_center;
}

INLINE bool LUIBaseElement::is_horizontal_centered() {
  return _placement_x == M_center;
}

INLINE void LUIBaseElement::set_margin(const LVector4 &margin) {
  _margin->set_bounds(margin);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin(float top, float right, float bottom, float left) {
  _margin->set_bounds(top, right, bottom, left);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_top(float top) {
  _margin->set_top(top);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_right(float right) {
  _margin->set_right(right);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_bottom(float bottom) {
  _margin->set_bottom(bottom);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_left(float left) {
  _margin->set_left(left);
  recompute_position();
}

INLINE float LUIBaseElement::get_margin_top() {
  return _margin->get_top();
}

INLINE float LUIBaseElement::get_margin_right() {
  return _margin->get_right();
}

INLINE float LUIBaseElement::get_margin_bottom() {
  return _margin->get_bottom();
}

INLINE float LUIBaseElement::get_margin_left() {
  return _margin->get_left();
}

INLINE LUIBounds *LUIBaseElement::get_margin() {
  return _margin;
}

INLINE void LUIBaseElement::set_padding(const LVector4 &padding) {
  _padding->set_bounds(padding);
  recompute_position();
}

INLINE void LUIBaseElement::set_padding(float top, float right, float bottom, float left) {
  _padding->set_bounds(top, right, bottom, left);
  recompute_position();
}

INLINE void LUIBaseElement::set_padding_top(float top) {
  _padding->set_top(top);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_right(float right) {
  _padding->set_right(right);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_bottom(float bottom) {
  _padding->set_bottom(bottom);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_left(float left) {
  _padding->set_left(left);
  recompute_position();
}

INLINE float LUIBaseElement::get_padding_top() {
  return _padding->get_top();
}

INLINE float LUIBaseElement::get_padding_right() {
  return _padding->get_right();
}

INLINE float LUIBaseElement::get_padding_bottom() {
  return _padding->get_bottom();
}

INLINE float LUIBaseElement::get_padding_left() {
  return _padding->get_left();
}

INLINE LUIBounds *LUIBaseElement::get_padding() {
  return _padding;
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
  return _size.get_x() > 0.0 && _size.get_y() > 0.0;
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

INLINE void LUIBaseElement::set_visible(bool visible) {
  _visible = visible;
  recompute_position();
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

INLINE void LUIBaseElement::set_z_offset(int z_offset) {
  _local_z_index = (float)z_offset;
  recompute_z_index();
}

INLINE float LUIBaseElement::get_z_offset() {
  return _local_z_index;
}

INLINE float LUIBaseElement::get_abs_z_offset() {
  return _z_index;
}

INLINE bool LUIBaseElement::has_focus() {
  return _focused;
}

INLINE LUIBaseElement* LUIBaseElement::get_parent() {
  return _parent;
}

INLINE bool LUIBaseElement::intersects(float x, float y) {
  return (
      x >= _pos_x && y >= _pos_y &&
      x <= _pos_x + _size.get_x() && y <= _pos_y + _size.get_y()
    );
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
    luiBaseElement_cat.spam() << _debug_name << "End of update section .." << endl;
  }
  recompute_position();

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << _debug_name << "Finally left update section .." << endl;
  }
}

INLINE void LUIBaseElement::set_clip_bounds(LUIBounds *bounds) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << _debug_name << "Setting clip bounds to (" << bounds->get_top() << ", " << bounds->get_right() << " / " << bounds->get_bottom() << " x " << bounds->get_left() << ") .." << endl;
  }
  _clip_bounds = new LUIBounds(bounds->get_bounds());
  recompute_position();
}

INLINE void LUIBaseElement::set_clip_bounds(float top, float right, float bottom, float left) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << _debug_name << "Setting clip bounds to (" << top << ", " << right << " / " << bottom << " x " << left << ") .." << endl;
  }
  _clip_bounds = new LUIBounds(top, right, bottom, left);
  recompute_position();
}

INLINE LUIBounds *LUIBaseElement::get_clip_bounds() {
  return _clip_bounds;
}

INLINE LUIRect *LUIBaseElement::get_abs_clip_bounds() {
  return _abs_clip_bounds;
}



INLINE void LUIBaseElement::set_parent(LUIBaseElement* parent) {
  _parent = parent;
}

INLINE void LUIBaseElement::set_focus(bool focus) {
  _focused = focus;
}

INLINE float LUIBaseElement::get_parent_width() {
  if (_parent == NULL) {
    return 0.0;
  }
  return _parent->get_width();
}

INLINE float LUIBaseElement::get_parent_height() {
  if (_parent == NULL) { 
    return 0.0;
  }
  return _parent->get_height(); 
}

INLINE void LUIBaseElement::recompute_z_index() {
  if (_parent != NULL) {
    _z_index = _parent->get_abs_z_offset() + _local_z_index;
    nassertv(_z_index > -10000.0 && _z_index < 10000.0);
  } else {
    _z_index = _local_z_index;
  }
  on_z_index_changed();
}

INLINE void LUIBaseElement::on_color_changed() {
  if (_parent != NULL) {
    compose_color(_parent->get_composed_color());
  } else {
    compose_color();
  }
}

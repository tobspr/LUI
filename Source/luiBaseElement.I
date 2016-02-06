

INLINE void LUIBaseElement::bind(const string &event_name, CallbackObject* callback) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Binding event '" << event_name << "'" << endl;
  }
  if (_events.count(event_name) != 0) {
    lui_cat.warning() << "Overriding event handler for '" << event_name << "'" << endl;
  }

  _events[event_name] = callback;
}

INLINE void LUIBaseElement::unbind(const string &event_name) {
  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Unbinding event '" << event_name << "'" << endl;
  }

  const auto elem_it = _events.find(event_name);
  if (elem_it != _events.end()) {
    _events.erase(elem_it);
  }
}

INLINE void LUIBaseElement::unbind_all() {
  _events.clear();
}

INLINE bool LUIBaseElement::has_event(const string &event_name) {
  return _events.count(event_name) > 0;
}

INLINE void LUIBaseElement::set_snap_position(bool snap) {
  _snap_position = snap;
}

INLINE void LUIBaseElement::set_top_left(const LPoint2 &pos) {
  _placement.x = M_default;
  _placement.y = M_default;
  _position = pos;
}

INLINE void LUIBaseElement::set_top_right(const LPoint2 &pos) {
  _placement.x = M_inverse;
  _placement.y = M_default;
  _position = pos;
}

INLINE void LUIBaseElement::set_bottom_left(const LPoint2 &pos) {
  _placement.x = M_default;
  _placement.y = M_inverse;
  _position = pos;
}

INLINE void LUIBaseElement::set_bottom_right(const LPoint2 &pos) {
  _placement.x = M_inverse;
  _placement.y = M_inverse;
  _position = pos;
}

INLINE LPoint2 LUIBaseElement::get_top_left() const {
  return LPoint2(get_left(), get_top());
}

INLINE LPoint2 LUIBaseElement::get_top_right() const {
  return LPoint2(get_right(), get_top());
}

INLINE LPoint2 LUIBaseElement::get_bottom_left() const {
  return LPoint2(get_left(), get_bottom());
}

INLINE LPoint2 LUIBaseElement::get_bottom_right() const {
  return LPoint2(get_right(), get_bottom());
}

INLINE void LUIBaseElement::set_pos(const LPoint2 &pos) {
  set_pos(pos.get_x(), pos.get_y());
}

INLINE void LUIBaseElement::set_pos(float x, float y) {
  set_top_left(LPoint2(x, y));
}

INLINE LPoint2 LUIBaseElement::get_pos() const {
  return get_top_left();
}

INLINE LPoint2 LUIBaseElement::get_abs_pos() const {
  return _abs_position;
}

INLINE void LUIBaseElement::set_top(float top) {
  _placement.y = M_default;
  _position.set_y(top);
}

INLINE void LUIBaseElement::set_right(float right) {
  _placement.x = M_inverse;
  _position.set_x(right);
}

INLINE void LUIBaseElement::set_bottom(float bottom) {
  _placement.y = M_inverse;
  _position.set_y(bottom);
}

INLINE void LUIBaseElement::set_left(float left) {
  _placement.x = M_default;
  _position.set_x(left);
}

INLINE float LUIBaseElement::get_top() const {
  return _position.get_y();
}

INLINE float LUIBaseElement::get_right() const {
  return _position.get_x();
}

INLINE float LUIBaseElement::get_bottom() const {
  return _position.get_y();
}

INLINE float LUIBaseElement::get_left() const {
  return _position.get_x();
}

INLINE void LUIBaseElement::set_centered(bool center_vert, bool center_horiz) {
  if (center_horiz) {
    _placement.x = M_center;
    _position.set_x(0.0f);
  }

  if (center_vert) {
    _placement.y = M_center;
    _position.set_y(0.0f);
  }

  if (!center_vert && !center_horiz) {
    luiBaseElement_cat.warning() << "set_centered() called, but no parameter was true. To un-center an "
                                 << "element, use the top_left property for example instead." << endl;
  }
}

INLINE void LUIBaseElement::set_center_vertical(bool centered) {
  if (centered) {
    _placement.y = M_center;
    _position.set_y(0.0f);
  } else {
    luiBaseElement_cat.warning() << "set_center_vertical called with false as argument, this has no effect!" << endl;
  }
}

INLINE void LUIBaseElement::set_center_horizontal(bool centered) {
  if (centered) {
    _placement.x = M_center;
    _position.set_x(0.0f);
  } else {
    luiBaseElement_cat.warning() << "set_center_horizontal called with false as argument, this has no effect!" << endl;
  }
}

INLINE bool LUIBaseElement::is_centered() const {
  return _placement.x == M_center && _placement.y == M_center;
}

INLINE bool LUIBaseElement::is_vertical_centered() const {
  return _placement.y == M_center;
}

INLINE bool LUIBaseElement::is_horizontal_centered() const {
  return _placement.x == M_center;
}

INLINE void LUIBaseElement::set_margin(const LVector4 &margin) {
  _margin.set_bounds(margin);
}

INLINE void LUIBaseElement::set_margin(float top, float right, float bottom, float left) {
  _margin.set_bounds(top, right, bottom, left);
}

INLINE void LUIBaseElement::set_margin(float margin) {
  _margin.set_bounds(margin, margin, margin, margin);
}


INLINE void LUIBaseElement::set_margin_top(float top) {
  _margin.set_top(top);
}

INLINE void LUIBaseElement::set_margin_right(float right) {
  _margin.set_right(right);
}

INLINE void LUIBaseElement::set_margin_bottom(float bottom) {
  _margin.set_bottom(bottom);
}

INLINE void LUIBaseElement::set_margin_left(float left) {
  _margin.set_left(left);
}

INLINE float LUIBaseElement::get_margin_top() const {
  return _margin.get_top();
}

INLINE float LUIBaseElement::get_margin_right() const {
  return _margin.get_right();
}

INLINE float LUIBaseElement::get_margin_bottom() const {
  return _margin.get_bottom();
}

INLINE float LUIBaseElement::get_margin_left() const {
  return _margin.get_left();
}

INLINE const LUIBounds& LUIBaseElement::get_margin() const {
  return _margin;
}

INLINE void LUIBaseElement::set_padding(const LVector4 &padding) {
  _padding.set_bounds(padding);
}

INLINE void LUIBaseElement::set_padding(float top, float right, float bottom, float left) {
  _padding.set_bounds(top, right, bottom, left);
}

INLINE void LUIBaseElement::set_padding(float padding) {
  _padding.set_bounds(padding, padding, padding, padding);
}

INLINE void LUIBaseElement::set_padding_top(float top) {
  _padding.set_top(top);
}

INLINE void LUIBaseElement::set_padding_right(float right) {
  _padding.set_right(right);
}

INLINE void LUIBaseElement::set_padding_bottom(float bottom) {
  _padding.set_bottom(bottom);
}

INLINE void LUIBaseElement::set_padding_left(float left) {
  _padding.set_left(left);
}

INLINE float LUIBaseElement::get_padding_top() const {
  return _padding.get_top();
}

INLINE float LUIBaseElement::get_padding_right() const {
  return _padding.get_right();
}

INLINE float LUIBaseElement::get_padding_bottom() const {
  return _padding.get_bottom();
}

INLINE float LUIBaseElement::get_padding_left() const {
  return _padding.get_left();
}

INLINE const LUIBounds& LUIBaseElement::get_padding() const {
  return _padding;
}

INLINE void LUIBaseElement::set_size(const LVector2 &size) {
  set_size(size.get_x(), size.get_y());
}

INLINE void LUIBaseElement::set_size(float width, float height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

INLINE void LUIBaseElement::set_size(const string& width, const string& height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

INLINE void LUIBaseElement::set_size(const string& width, float height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

INLINE void LUIBaseElement::set_size(float width, const string& height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

INLINE bool LUIBaseElement::has_size() const {
  return _size.x.has_expression() && _size.y.has_expression();
}

INLINE void LUIBaseElement::set_width(float width) {
  _size.x.load_expression(width);
}

INLINE void LUIBaseElement::set_width(const string& width) {
  _size.x.load_expression(width);
}

INLINE void LUIBaseElement::set_height(float height) {
  _size.y.load_expression(height);
}

INLINE void LUIBaseElement::set_height(const string& height) {
  _size.y.load_expression(height);
}

INLINE float LUIBaseElement::get_width() const {
  if (_size.x.has_fixed_expression()) return _size.x.evaluate(0.0f);
  return _effective_size.get_x();
}

INLINE float LUIBaseElement::get_height() const {
  if (_size.y.has_fixed_expression()) return _size.y.evaluate(0.0f);
  return _effective_size.get_y();
}

INLINE LVector2 LUIBaseElement::get_size() const {
  return LVector2(get_width(), get_height());
}

INLINE void LUIBaseElement::set_visible(bool visible) {
  _visible = visible;
}

INLINE bool LUIBaseElement::is_visible() const {
  return _visible;
}

INLINE void LUIBaseElement::hide() {
  set_visible(false);
}

INLINE void LUIBaseElement::show() {
  set_visible(true);
}

INLINE float LUIBaseElement::get_z_offset() const {
  return _z_offset;
}

INLINE bool LUIBaseElement::has_focus() const {
  return _focused;
}

INLINE bool LUIBaseElement::has_parent() const {
  return _parent != NULL;
}

INLINE LUIObject* LUIBaseElement::get_parent() const {
  return _parent;
}

INLINE bool LUIBaseElement::intersects(float x, float y) const {
  return (
      x >= _abs_position.get_x() &&
      y >= _abs_position.get_y() &&
      x <= _abs_position.get_x() + _effective_size.get_x() &&
      y <= _abs_position.get_y() + _effective_size.get_y() &&

      x >= _abs_clip_bounds.get_x() &&
      y >= _abs_clip_bounds.get_y() &&
      x <= _abs_clip_bounds.get_x() + _abs_clip_bounds.get_w() &&
      y <= _abs_clip_bounds.get_y() + _abs_clip_bounds.get_h()
    );
}

INLINE void LUIBaseElement::clear_clip_bounds() {
  _have_clip_bounds = false;
}

INLINE void LUIBaseElement::set_clip_bounds(const LUIBounds& bounds) {
  _clip_bounds = bounds;
  _have_clip_bounds = true;
}

INLINE void LUIBaseElement::set_clip_bounds(float top, float right, float bottom, float left) {
  _clip_bounds.set_bounds(top, right, bottom, left);
  _have_clip_bounds = true;
}

INLINE const LUIBounds& LUIBaseElement::get_clip_bounds() const {
  return _clip_bounds;
}

INLINE const LUIRect& LUIBaseElement::get_abs_clip_bounds() const {
  return _abs_clip_bounds;
}

INLINE void LUIBaseElement::do_set_parent(LUIObject* parent) {
  _parent = parent;
}

INLINE void LUIBaseElement::set_focus(bool focus) {
  _focused = focus;
}

INLINE int LUIBaseElement::get_last_frame_visible() const {
  return _last_frame_visible;
}

INLINE bool LUIBaseElement::is_topmost() const {
  return _topmost;
}

INLINE void LUIBaseElement::set_topmost(bool topmost) {
  _topmost = topmost;
}


INLINE LVector2 LUIBaseElement::get_relative_pos(const LPoint2& pos) const {
  return _abs_position - pos;
}


INLINE int LUIBaseElement::get_last_render_index() const {
  return _last_render_index;
}

INLINE void LUIBaseElement::set_solid(bool solid) {
  _solid = solid;
  if (_solid) {
    register_events();
  } else {
    unregister_events();
  }
}

INLINE bool LUIBaseElement::get_solid() const {
  return _solid;
}

INLINE float LUIBaseElement::get_x_extent() const {
  return _abs_position.get_x() + _effective_size.get_x() + _margin.get_right();
}

INLINE float LUIBaseElement::get_y_extent() const {
  return _abs_position.get_y() + _effective_size.get_y() + _margin.get_bottom();
}

INLINE void LUIBaseElement::set_debug_name(const string& debug_name) {
  _debug_name = debug_name;
}

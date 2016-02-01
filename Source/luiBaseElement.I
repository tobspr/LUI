

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
  recompute_position();
}

INLINE void LUIBaseElement::set_top_left(const LPoint2 &pos) {
  _placement_x = M_default;
  _placement_y = M_default;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_top_right(const LPoint2 &pos) {
  _placement_x = M_inverse;
  _placement_y = M_default;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_bottom_left(const LPoint2 &pos) {
  _placement_x = M_default;
  _placement_y = M_inverse;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
}

INLINE void LUIBaseElement::set_bottom_right(const LPoint2 &pos) {
  _placement_x = M_inverse;
  _placement_y = M_inverse;
  _offset_x = pos.get_x();
  _offset_y = pos.get_y();
  recompute_position();
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

INLINE float LUIBaseElement::get_top() const {
  return _rel_pos_y;
}

INLINE float LUIBaseElement::get_right() const {
  return get_parent_width() - get_left();
}

INLINE float LUIBaseElement::get_bottom() const {
  return get_parent_height() - get_top();
}

INLINE float LUIBaseElement::get_left() const {
  return _rel_pos_x;
}

INLINE LPoint2 LUIBaseElement::get_relative_pos(const LPoint2 &abs_pos) const {
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

  recompute_position();
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

INLINE bool LUIBaseElement::is_centered() const {
  return _placement_x == M_center && _placement_y == M_center;
}

INLINE bool LUIBaseElement::is_vertical_centered() const {
  return _placement_y == M_center;
}

INLINE bool LUIBaseElement::is_horizontal_centered() const {
  return _placement_x == M_center;
}

INLINE void LUIBaseElement::set_margin(const LVector4 &margin) {
  _margin.set_bounds(margin);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin(float top, float right, float bottom, float left) {
  _margin.set_bounds(top, right, bottom, left);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin(float margin) {
  _margin.set_bounds(margin, margin, margin, margin);
  recompute_position();
}


INLINE void LUIBaseElement::set_margin_top(float top) {
  _margin.set_top(top);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_right(float right) {
  _margin.set_right(right);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_bottom(float bottom) {
  _margin.set_bottom(bottom);
  recompute_position();
}

INLINE void LUIBaseElement::set_margin_left(float left) {
  _margin.set_left(left);
  recompute_position();
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
  recompute_position();
}

INLINE void LUIBaseElement::set_padding(float top, float right, float bottom, float left) {
  _padding.set_bounds(top, right, bottom, left);
  recompute_position();
}

INLINE void LUIBaseElement::set_padding(float padding) {
  _padding.set_bounds(padding, padding, padding, padding);
  recompute_position();
}

INLINE void LUIBaseElement::set_padding_top(float top) {
  _padding.set_top(top);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_right(float right) {
  _padding.set_right(right);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_bottom(float bottom) {
  _padding.set_bottom(bottom);
  recompute_position();
}
INLINE void LUIBaseElement::set_padding_left(float left) {
  _padding.set_left(left);
  recompute_position();
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


INLINE void LUIBaseElement::set_size(float w, float h) {
  if (_snap_position) {
    w = ceil(w);
    h = ceil(h);
  }
  _size_x.load_expression(w);
  _size_y.load_expression(h);
  recompute_position();
}


INLINE void LUIBaseElement::set_size(const string& w, const string& h) {
  _size_x.load_expression(w);
  _size_y.load_expression(h);
  recompute_position();
}

INLINE void LUIBaseElement::set_size(const string& w, float h) {
  if (_snap_position)
    h = ceil(h);
  _size_x.load_expression(w);
  _size_y.load_expression(h);
  recompute_position();
}


INLINE void LUIBaseElement::set_size(float w, const string& h) {
  if (_snap_position)
    w = ceil(w);
  _size_x.load_expression(w);
  _size_y.load_expression(h);
  recompute_position();
}

INLINE bool LUIBaseElement::has_size() const {
  return _effective_size.get_x() > 0.0f && _effective_size.get_y() > 0.0f;
}

INLINE void LUIBaseElement::set_width(float w) {
  if (_snap_position)
    w = ceil(w);
  _size_x.load_expression(w);
  recompute_position();
}

INLINE void LUIBaseElement::set_width(const string& w) {
  _size_x.load_expression(w);
  recompute_position();
}

INLINE void LUIBaseElement::set_height(float h) {
  if (_snap_position)
    h = ceil(h);
  _size_y.load_expression(h);
  recompute_position();
}

INLINE void LUIBaseElement::set_height(const string& h) {
  _size_y.load_expression(h);
  recompute_position();
}

INLINE float LUIBaseElement::get_width() const {
  return _effective_size.get_x();
}

INLINE float LUIBaseElement::get_height() const {
  return _effective_size.get_y();
}

INLINE const LVector2& LUIBaseElement::get_size() const {
  return _effective_size;
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
      x >= _pos_x &&
      y >= _pos_y &&
      x <= _pos_x + _effective_size.get_x() &&
      y <= _pos_y + _effective_size.get_y() &&

      x >= _abs_clip_bounds.get_x() &&
      y >= _abs_clip_bounds.get_y() &&
      x <= _abs_clip_bounds.get_x() + _abs_clip_bounds.get_w() &&
      y <= _abs_clip_bounds.get_y() + _abs_clip_bounds.get_h()
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
    luiBaseElement_cat.spam() << "End of update section .." << endl;
  }

  recompute_position();

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Finally left update section .." << endl;
  }
}

INLINE void LUIBaseElement::clear_clip_bounds() {
  _have_clip_bounds = false;
  recompute_position();
}

INLINE void LUIBaseElement::set_clip_bounds(const LUIBounds& bounds) {
  _clip_bounds = bounds;
  _have_clip_bounds = true;
  recompute_position();
}

INLINE void LUIBaseElement::set_clip_bounds(float top, float right, float bottom, float left) {
  _clip_bounds.set_bounds(top, right, bottom, left);
  _have_clip_bounds = true;
  recompute_position();
}

INLINE const LUIBounds& LUIBaseElement::get_clip_bounds() const {
  return _clip_bounds;
}

INLINE const LUIRect& LUIBaseElement::get_abs_clip_bounds() const {
  return _abs_clip_bounds;
}

INLINE void LUIBaseElement::do_set_parent(LUIObject* parent) {
  _parent = parent;
  recompute_position();
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

INLINE void LUIBaseElement::set_emits_changed_event(bool emit){
  _emits_changed_event = emit;
}

INLINE bool LUIBaseElement::get_emits_changed_event() const {
  return _emits_changed_event;
}

INLINE bool LUIBaseElement::contributes_to_fluid_width() const {
  return _placement_x == M_default;
}

INLINE bool LUIBaseElement::contributes_to_fluid_height() const {
  return _placement_y == M_default;
}

INLINE float LUIBaseElement::get_inner_width() {
  return _effective_size.get_x() - _padding.get_left() - _padding.get_right();
}

INLINE float LUIBaseElement::get_inner_height() {
  return _effective_size.get_y() - _padding.get_top() - _padding.get_bottom();
}

INLINE float LUIBaseElement::get_x_extent() {
  return _pos_x + _effective_size.get_x() + _margin.get_right();
}

INLINE float LUIBaseElement::get_y_extent() {
  return _pos_y + _effective_size.get_y() + _margin.get_bottom();
}


INLINE float LUIBounds::get_top() const {
  return _bounds.get_x();
}

INLINE float LUIBounds::get_right() const {
  return _bounds.get_y();
}

INLINE float LUIBounds::get_bottom() const {
  return _bounds.get_z();
}

INLINE float LUIBounds::get_left() const {
  return _bounds.get_w();
}

INLINE void LUIBounds::set_top(float top) {
  _bounds.set_x(top);
}

INLINE void LUIBounds::set_right(float right) {
  _bounds.set_y(right);
}

INLINE void LUIBounds::set_bottom(float bottom) {
  _bounds.set_z(bottom);
}

INLINE void LUIBounds::set_left(float left) {
  _bounds.set_w(left);
}

INLINE void LUIBounds::set_bounds(const LVector4& bounds) {
  _bounds = LVector4(bounds);
}

INLINE void LUIBounds::set_bounds(float top, float right, float bottom, float left) {
  _bounds.set_x(top);
  _bounds.set_y(right);
  _bounds.set_z(bottom);
  _bounds.set_w(left);
}

INLINE const LVector4& LUIBounds::get_bounds() const {
  return _bounds;
}

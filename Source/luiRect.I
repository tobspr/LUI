
INLINE float LUIRect::get_x() {
  return _rect.get_x();
}

INLINE float LUIRect::get_y() {
  return _rect.get_y();
}

INLINE float LUIRect::get_w() {
  return _rect.get_z();
}

INLINE float LUIRect::get_h() {
  return _rect.get_w();
}

INLINE void LUIRect::set_x(float x) {
  _rect.set_x(x);
}

INLINE void LUIRect::set_y(float y) {
  _rect.set_y(y);
}

INLINE void LUIRect::set_w(float w) {
  _rect.set_z(w);
}

INLINE void LUIRect::set_h(float h) {
  _rect.set_w(h);
}

INLINE void LUIRect::set_rect(const LVector4 &rect) {
  _rect = rect;
}

INLINE void LUIRect::set_rect(float x, float y, float w, float h) {
  _rect.set_x(x);
  _rect.set_y(y);
  _rect.set_z(w);
  _rect.set_w(h);
}

INLINE const LVector4 &LUIRect::get_rect() {
  return _rect;
}
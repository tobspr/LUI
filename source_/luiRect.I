
INLINE float LUIRect::get_x() const {
  return _rect.get_x();
}

INLINE float LUIRect::get_y() const {
  return _rect.get_y();
}

INLINE float LUIRect::get_w() const {
  return _rect.get_z();
}

INLINE float LUIRect::get_h() const {
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

INLINE void LUIRect::set_rect(const LVector4& rect) {
  _rect = rect;
}

INLINE void LUIRect::set_rect(const LVector2& xy, const LVector2& wh) {
  _rect.set(xy.get_x(), xy.get_y(), wh.get_x(), wh.get_y());
}

INLINE void LUIRect::set_rect(float x, float y, float w, float h) {
  _rect.set(x, y, w, h);
}

INLINE const LVector4& LUIRect::get_rect() const {
  return _rect;
}

INLINE LVector2 LUIRect::get_xy() const {
  return LVector2(_rect.get_x(), _rect.get_y());
}

INLINE LVector2 LUIRect::get_wh() const {
  return LVector2(_rect.get_z(), _rect.get_w());
}

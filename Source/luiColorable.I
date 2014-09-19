

INLINE void LUIColorable::set_color(const LColor &color) {
  _color = color;
  on_color_changed();
}

INLINE void LUIColorable::set_color(const LVector3 &color) {
  _color.set_x(color.get_x());
  _color.set_y(color.get_y());
  _color.set_z(color.get_z());
  on_color_changed();
}

INLINE void LUIColorable::set_color(float r, float g, float b, float a) {
  _color.set_x(r);
  _color.set_y(g);
  _color.set_z(b);
  _color.set_w(a);
  on_color_changed();
}

INLINE void LUIColorable::set_red(float r) {
  _color.set_x(r);
  on_color_changed();
}

INLINE void LUIColorable::set_green(float g) {
  _color.set_y(g);
  on_color_changed();
}

INLINE void LUIColorable::set_blue(float b) {
  _color.set_z(b);
  on_color_changed();
}

INLINE void LUIColorable::set_alpha(float a) {
  _color.set_w(a);
  on_color_changed();
}

INLINE float LUIColorable::get_red() {
  return _color.get_x();
}

INLINE float LUIColorable::get_green() {
  return _color.get_y();
}

INLINE float LUIColorable::get_blue() {
  return _color.get_z();
}

INLINE float LUIColorable::get_alpha() {
  return _color.get_w();
}

INLINE const LColor &LUIColorable::get_color() {
  return _color;
}

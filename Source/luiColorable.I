

INLINE void LUIColorable::set_color(const LColor& color) {
  _color = color;
}

INLINE void LUIColorable::set_color(const LVecBase3& rgb) {
  _color.set_x(rgb.get_x());
  _color.set_y(rgb.get_y());
  _color.set_z(rgb.get_z());
}

INLINE void LUIColorable::set_color(float r, float g, float b, float a) {
  _color.set(r, g, b, a);
}

INLINE void LUIColorable::set_red(float r) {
  _color.set_x(r);
}

INLINE void LUIColorable::set_green(float g) {
  _color.set_y(g);
}

INLINE void LUIColorable::set_blue(float b) {
  _color.set_z(b);
}

INLINE void LUIColorable::set_alpha(float a) {
  _color.set_w(a);
}

INLINE float LUIColorable::get_red() const {
  return _color.get_x();
}

INLINE float LUIColorable::get_green() const {
  return _color.get_y();
}

INLINE float LUIColorable::get_blue() const {
  return _color.get_z();
}

INLINE float LUIColorable::get_alpha() const {
  return _color.get_w();
}

INLINE const LColor& LUIColorable::get_color() const {
  return _color;
}

INLINE const LColor& LUIColorable::get_composed_color() const {
  return _composed_color;
}

INLINE void LUIColorable::compose_color(const LColor& parent_color) {
  _composed_color = LColor(
    parent_color.get_x() * _color.get_x(),
    parent_color.get_y() * _color.get_y(),
    parent_color.get_z() * _color.get_z(),
    parent_color.get_w() * _color.get_w()
  );
}

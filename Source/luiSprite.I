

INLINE void LUISprite::set_pos(const LPoint2 &pos) {
  set_pos(pos.get_x(), pos.get_y());
}

INLINE void LUISprite::set_pos(float x, float y) {
  if (!is_valid_coord(x, y)) {
    lui_cat.warning() << "Non-pixel position detected!\n";
  }
  _data[0].x = x;
  _data[0].y = y;
  update_vertices();
}


INLINE LPoint2 LUISprite::get_pos() {
  return LPoint2(_data[0].x, _data[0].y);
}

INLINE void LUISprite::set_size(const LVector2 &size) {
  set_size(size.get_x(), size.get_y());
}

INLINE void LUISprite::set_size(float x, float y) {
  if (!is_valid_coord(x, y)) {
    lui_cat.warning() << "Non-pixel size detected!\n";
  }
  _size.set_x(x);
  _size.set_y(y);
  update_vertices();
}

INLINE void LUISprite::update_vertices() {
  // Upper Right
  _data[1].x = _data[0].x + _size.get_x();
  _data[1].y = _data[0].y;
      
  // Lower Right
  _data[2].x =_data[0].x + _size.get_x();
  _data[2].y =_data[0].y + _size.get_y();

  // Lower Left
  _data[3].x = _data[0].x;
  _data[3].y = _data[0].y + _size.get_y();
}

INLINE const LVector2 &LUISprite::get_size() const {
    return _size;
}

INLINE void LUISprite::set_texcoord_start(const LVector2 &texcoord_start) {
  set_texcoord_start(texcoord_start.get_x(), texcoord_start.get_y());
}

INLINE void LUISprite::set_texcoord_start(float u, float v) {
  if (!is_valid_coord(u, v)) {
    lui_cat.warning() << "Non-pixel texcoord (start) detected!\n";
  }
  _data[0].u = u;
  _data[3].u = u;
  _data[0].v = v;
  _data[1].v = v;
}

INLINE LVector2 LUISprite::get_texcoord_start() {
  return LVector2(_data[0].u, _data[0].v);
}

INLINE void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
  set_texcoord_end(texcoord_end.get_x(), texcoord_end.get_y());
}

INLINE void LUISprite::set_texcoord_end(float u, float v) {
  if (!is_valid_coord(u, v)) {
    lui_cat.warning() << "Non-pixel texcoord (end) detected!\n";
  }
  _data[2].u = u;
  _data[1].u = u;
  _data[2].v = v;
  _data[3].v = v;
}

INLINE LVector2 LUISprite::get_texcoord_end() {
    return LVector2(_data[2].u, _data[2].v);
}
		
INLINE void LUISprite::set_color(const LColor &color) {
  set_color(color.get_x(), color.get_y(), color.get_z(), color.get_w());
}

INLINE void LUISprite::set_color(float r, float g, float b, float a) {
  for (int i = 0; i < 4; i++) {
    _data[i].color[0] = r;
    _data[i].color[1] = g;
    _data[i].color[2] = b;
    _data[i].color[3] = a;
  }
}

INLINE LColor LUISprite::get_color() {
  return LColor(
    _data[0].color[0], 
    _data[0].color[1], 
    _data[0].color[2],
    _data[0].color[3]);
}

INLINE void LUISprite::set_texture(Texture* tex) {
  lui_cat.error() << "set_texture is not implemented yet\n";
}

INLINE Texture* LUISprite::get_texture() const {
  lui_cat.error() << "get_texture is not implemented yet\n";
  return NULL;
}

INLINE void LUISprite::set_z_index(float z_index) {
  for (int i = 0; i < 4; i++) {
    _data[i].z = z_index;
  }
}

INLINE float LUISprite::get_z_index() {
  return _data[0].z;
}
		
INLINE void LUISprite::set_visible(bool visible) {
  _visible = visible;
}

INLINE bool LUISprite::is_visible() {
  return _visible;
}

INLINE void LUISprite::hide() {
  set_visible(false);
}

INLINE void LUISprite::show() {
  set_visible(true);
}

INLINE void LUISprite::set_pool_slot(int slot) {
  _pool_slot = slot;
}

INLINE int LUISprite::get_pool_slot() {
  return _pool_slot;
}

INLINE bool LUISprite::is_valid_coord(float x, float y) {
  return fmod(x, 1.0) == 0.0 && fmod(y, 1.0) == 0.0;
}

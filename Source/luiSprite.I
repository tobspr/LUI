

INLINE void LUISprite::set_pos(const LPoint2 &pos) {
    // Upper Left
    _data[0].x = pos.get_x();
    _data[0].y = pos.get_y();
    update_vertices();
}

INLINE const LPoint2 &LUISprite::get_pos() const {
    return NULL; // Todo
}

INLINE void LUISprite::set_size(const LVector2 &size) {
    _size = size;
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
  _data[0].u = texcoord_start.get_x();
  _data[3].u = texcoord_start.get_x();
  _data[0].v = texcoord_start.get_y();
  _data[1].v = texcoord_start.get_y();
}

INLINE const LVector2 &LUISprite::get_texcoord_start() const {
    return NULL; // Todo
}

INLINE void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
  _data[2].u = texcoord_end.get_x();
  _data[1].u = texcoord_end.get_x();
  _data[2].v = texcoord_end.get_y();
  _data[3].v = texcoord_end.get_y();
}

INLINE const LVector2 &LUISprite::get_texcoord_end() const {
    return NULL; // Todo
}
		
INLINE void LUISprite::set_color(const LColor &color) {
    for (int i = 0; i < 4; i++) {
      _data[i].col[0] = color.get_x();
      _data[i].col[1] = color.get_y();
      _data[i].col[2] = color.get_z();
      _data[i].col[3] = color.get_w();
    }
}

INLINE const LColor &LUISprite::get_color() const {
    return NULL; // Todo
}

INLINE void LUISprite::set_texture(Texture* tex) {
  // Todo
}

INLINE Texture* LUISprite::get_texture() const {
    return NULL; // Todo
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
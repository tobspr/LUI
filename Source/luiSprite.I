

INLINE void LUISprite::set_pos(const LPoint2 &pos) {
  
  // Upper Left
  _data[0].x = pos.get_x();
  _data[0].y = pos.get_y();
 
  // Works
  cout << "Set position (cout): " << 5 << "\n";

  cout << "Locale: " << cout.getloc().name().c_str() << "\n";

  // Crashes
  // Access violation reading 0xFFFFFFFFFFFFFFFF
  lui_cat.error() << "Set position (lui_cat): " << 5 << "\n";

  update_vertices();
}

INLINE LPoint2 LUISprite::get_pos() {
  return LPoint2(_data[0].x, _data[0].y);
}

INLINE void LUISprite::set_size(const LVector2 &size) {
  lui_cat.spam() << "Set size: " << size.get_x() << ", " << size.get_y() << "\n";
  _size = size;
  update_vertices();
}

INLINE void LUISprite::update_vertices() {
  lui_cat.spam() << "Updating vertices, based on _data[0] = " 
                  << _data[0].x << ", " << _data[0].y << " and size = "
                  << _size.get_x() << ", " << _size.get_y() << "\n";
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
  lui_cat.spam() << "Set texcoord start: " << texcoord_start.get_x() << ", " << texcoord_start.get_y() << "\n";
  _data[0].u = texcoord_start.get_x();
  _data[3].u = texcoord_start.get_x();
  _data[0].v = texcoord_start.get_y();
  _data[1].v = texcoord_start.get_y();
}

INLINE LVector2 LUISprite::get_texcoord_start() {
    return LVector2(_data[0].u, _data[0].v);
}

INLINE void LUISprite::set_texcoord_end(const LVector2 &texcoord_end) {
  lui_cat.spam() << "Set texcoord end: " << texcoord_end.get_x() << ", " << texcoord_end.get_y() << "\n";
  _data[2].u = texcoord_end.get_x();
  _data[1].u = texcoord_end.get_x();
  _data[2].v = texcoord_end.get_y();
  _data[3].v = texcoord_end.get_y();
}

INLINE LVector2 LUISprite::get_texcoord_end() {
    return LVector2(_data[2].u, _data[2].v);
}
		
INLINE void LUISprite::set_color(const LColor &color) {
  lui_cat.spam() << "Set color: (" << color.get_x() << ", " << color.get_y() << ", "
                 << color.get_z() << ", " << color.get_w() << "\n";
  for (int i = 0; i < 4; i++) {
    _data[i].col[0] = color.get_x();
    _data[i].col[1] = color.get_y();
    _data[i].col[2] = color.get_z();
    _data[i].col[3] = color.get_w();
  }
}

INLINE LColor LUISprite::get_color() {
  return LColor(
    _data[0].col[0], 
    _data[0].col[1], 
    _data[0].col[2],
    _data[0].col[3]);
}

INLINE void LUISprite::set_texture(Texture* tex) {
  lui_cat.error() << "set_texture is not implemented yet\n";
}

INLINE Texture* LUISprite::get_texture() const {
  lui_cat.error() << "get_texture is not implemented yet\n";
  return NULL;
}

INLINE void LUISprite::set_z_index(float z_index) {
  lui_cat.spam() << "Set z-index: " << z_index << "\n";
  for (int i = 0; i < 4; i++) {
    _data[i].z = z_index;
  }
}

INLINE float LUISprite::get_z_index() {
  return _data[0].z;
}
		
INLINE void LUISprite::set_visible(bool visible) {
  lui_cat.spam() << "Set visible: " << (visible?"true":"false") << "\n";
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
  lui_cat.spam() << "Set pool slot: " << slot << "\n";
  _pool_slot = slot;
}

INLINE int LUISprite::get_pool_slot() {
  return _pool_slot;
}
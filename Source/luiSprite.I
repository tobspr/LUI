

INLINE void LUISprite::recompute_vertices() {
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

INLINE void LUISprite::set_texcoord_start(const LVector2 &texcoord_start) {
  set_texcoord_start(texcoord_start.get_x(), texcoord_start.get_y());
}

INLINE void LUISprite::set_texcoord_start(float u, float v) {
  if (lui_cat.is_spam() && lui_cat.is_spam()) {
    cout << "Set texcoord start: " << u << " / " << v << endl;
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
  if (lui_cat.is_spam() && lui_cat.is_spam()) {
    cout << "Set texcoord end: " << u << " / " << v << endl;
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
  if (tex != NULL) {

    if (lui_cat.is_spam())
      cout << "Assigned texture of size " << tex->get_x_size() << "x" << tex->get_y_size() << endl;
    _tex = tex;

    set_texcoord_start(0, 0);
    set_texcoord_end(1, 1);
  }
}

INLINE void LUISprite::set_texture(LUIAtlasDescriptor *descriptor) {
  lui_cat.spam() << "LUISprite -> set texture from descriptor" << endl;

  if (descriptor == NULL) {
    lui_cat.spam() << "Ignoring null descriptor" << endl;
    return;
  }

  set_texture(descriptor->get_texture());
  set_size(descriptor->get_size());
  set_texcoord_start(descriptor->get_uv_begin());
  set_texcoord_end(descriptor->get_uv_end());
}

INLINE void LUISprite::set_texture(const string &source) {

  // load texture from file
  PT(Texture) tex = TexturePool::load_texture(source);

  if (tex == NULL) {
    lui_cat.error() << "Could not load " << source << endl;
    return;
  }

  set_texture(tex);
}

INLINE Texture *LUISprite::get_texture() const {
  return _tex;
}

INLINE void LUISprite::set_z_index(float z_index) {
  for (int i = 0; i < 4; i++) {
    _data[i].z = z_index;
  }
}

INLINE float LUISprite::get_z_index() {
  return _data[0].z;
}

INLINE void LUISprite::set_pool_slot(int slot) {
  _pool_slot = slot;
}

INLINE int LUISprite::get_pool_slot() {
  return _pool_slot;
}



INLINE void LUISprite::recompute_vertices() {
  // Upper Right
  _data[1].x = _data[0].x + _size.get_x();
  _data[1].z = _data[0].z;

  // Lower Right
  _data[2].x =_data[0].x + _size.get_x();
  _data[2].z =_data[0].z + _size.get_y();

  // Lower Left
  _data[3].x = _data[0].x;
  _data[3].z = _data[0].z + _size.get_y();
}

INLINE void LUISprite::set_uv_range(const LTexCoord &uv_begin, const LTexCoord &uv_end) {
  set_uv_range(uv_begin.get_x(), uv_begin.get_y(), uv_end.get_x(), uv_end.get_y());
}

INLINE void LUISprite::set_uv_range(float u0, float v0, float u1, float v1) {
  _data[0].u = u0;
  _data[0].v = 1-v0;

  _data[1].u = u1;
  _data[1].v = 1-v0;

  _data[2].u = u1;
  _data[2].v = 1-v1;

  _data[3].u = u0;
  _data[3].v = 1-v1;
  update_vertex_pool();
}


INLINE void LUISprite::get_uv_range(LTexCoord &uv_begin, LTexCoord &uv_end) {
  uv_begin.set_x(_data[0].u);
  uv_begin.set_y(1-_data[0].v);
  uv_end.set_x(_data[2].u);
  uv_end.set_y(1-_data[2].v);
}

INLINE void LUISprite::set_color(const LColor &color) {
  set_color(color.get_x(), color.get_y(), color.get_z(), color.get_w());
}

INLINE void LUISprite::set_color(float r, float g, float b, float a) {
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Setting color to RGBA(" << r << ", " << g << ", " << b << ", " << a << ")" << endl;
  }
  for (int i = 0; i < 4; i++) {
    _data[i].color[0] = (unsigned char) (r * 255.0);
    _data[i].color[1] = (unsigned char) (g * 255.0);
    _data[i].color[2] = (unsigned char) (b * 255.0);
    _data[i].color[3] = (unsigned char) (a * 255.0);
  }
  update_vertex_pool();

}

INLINE LColor LUISprite::get_color() {
  return LColor(
    _data[0].color[0] / 255.0, 
    _data[0].color[1] / 255.0, 
    _data[0].color[2] / 255.0,
    _data[0].color[3] / 255.0);
}

INLINE void LUISprite::set_texture(Texture* tex) {

  if (tex == _tex) {
    // No change
    return;
  }

  // Unassign old texture
  if (_tex != NULL && _chunk_descriptor != NULL) {
    unassign_vertex_pool();
    _tex = tex;
  }

  if (tex != NULL) {

    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() << "Assigned texture of size " << tex->get_x_size() << "x" << tex->get_y_size() << endl;
    }
    _tex = tex;
    set_uv_range(LTexCoord(0), LTexCoord(1));
    
    // Assign new pool
    if (_root != NULL) {
      assign_vertex_pool();
    }
  }
}

INLINE void LUISprite::set_texture(LUIAtlasDescriptor *descriptor) {

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Load texture data from descriptor" << endl;
  }

  nassertv(descriptor != NULL);

  set_texture(descriptor->get_texture());
  set_size(descriptor->get_size());
  set_uv_range(descriptor->get_uv_begin(), descriptor->get_uv_end());
}

INLINE void LUISprite::set_texture(const string &source) {

  // load texture from file
  PT(Texture) tex = TexturePool::load_texture(source);

  if (tex == NULL) {
    luiSprite_cat.error() << "Could not load texture from '" << source << "'" << endl;
    return;
  }

  set_texture(tex);
}

INLINE Texture *LUISprite::get_texture() const {
  return _tex;
}

INLINE void LUISprite::print_vertices() {
  cout << "LUISprite, 4 Vertices:" << endl;

  for (int i = 0; i < 4; i++) {
    cout << "  [Vertex] POS = " << _data[i].x << "," << _data[i].y << "," << _data[i].z 
      << "; UV = " << _data[i].u << "," << _data[i].v 
      << " COL = " << (float)_data[i].color[0] << "," << (float)_data[i].color[1] << "," << (float)_data[i].color[2] << "," << (float)_data[i].color[3] << endl;
  }

}

INLINE void LUISprite::end_update_section() {
  LUIBaseElement::end_update_section();

  // Sprite specific update stuff comes here
}

INLINE void LUISprite::set_red(float r) {
  for (int i = 0; i < 4; i++) {
    _data[i].color[0] = (unsigned char) (r * 255.0);
  }
  update_vertex_pool();
}

INLINE void LUISprite::set_green(float g) {
  for (int i = 0; i < 4; i++) {
    _data[i].color[1] = (unsigned char) (g * 255.0);
  }
  update_vertex_pool();
}

INLINE void LUISprite::set_blue(float b) {
  for (int i = 0; i < 4; i++) {
    _data[i].color[2] = (unsigned char) (b * 255.0);
  }
  update_vertex_pool();
}

INLINE void LUISprite::set_alpha(float a) {
  for (int i = 0; i < 4; i++) {
    _data[i].color[3] = (unsigned char) (a * 255.0);
  }
  update_vertex_pool();
}

INLINE float LUISprite::get_red() {
  return _data[0].color[0] / 255.0;
}

INLINE float LUISprite::get_green() {
  return _data[0].color[1] / 255.0;
}

INLINE float LUISprite::get_blue() {
  return _data[0].color[2] / 255.0;
}

INLINE float LUISprite::get_alpha() {
  return _data[0].color[3] / 255.0;
}




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
  _data[0].u = uv_begin.get_x();
  _data[0].v = uv_begin.get_y();

  _data[1].u = uv_end.get_x();
  _data[1].v = uv_begin.get_y();

  _data[2].u = uv_end.get_x();
  _data[2].v = uv_end.get_y();

  _data[3].u = uv_begin.get_x();
  _data[3].v = uv_end.get_y();
  update_vertex_pool();
}


INLINE void LUISprite::get_uv_range(LTexCoord &uv_begin, LTexCoord &uv_end) {
  uv_begin.set_x(_data[0].u);
  uv_begin.set_y(_data[0].v);
  uv_end.set_x(_data[2].u);
  uv_end.set_y(_data[2].v);
}

INLINE void LUISprite::set_color(const LColor &color) {
  set_color(color.get_x(), color.get_y(), color.get_z(), color.get_w());
}

INLINE void LUISprite::set_color(float r, float g, float b, float a) {
  if (lui_cat.is_spam()) {
    cout << "Setting color to RGBA(" << r << ", " << g << ", " << b << ", " << a << ")" << endl;
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

    if (lui_cat.is_spam()) {
      cout << "Assigned texture of size " << tex->get_x_size() << "x" << tex->get_y_size() << endl;
    }
    _tex = tex;
    set_uv_range(LTexCoord(0), LTexCoord(1));
    
    // Assign new texture
    if (_root != NULL) {

      if (lui_cat.is_spam()) {
        cout << "Assigning vertex pool from set_texture, as _tex is not NULL" << endl;
      }
      assign_vertex_pool();
    }
  }
}

INLINE void LUISprite::set_texture(LUIAtlasDescriptor *descriptor) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUISprite -> set texture from descriptor" << endl;
  }

  if (descriptor == NULL) {
    lui_cat.warning() << "Ignoring null descriptor" << endl;
    return;
  }

  set_texture(descriptor->get_texture());
  set_size(descriptor->get_size());
  set_uv_range(descriptor->get_uv_begin(), descriptor->get_uv_end());
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
    _data[i].y = z_index;
  }
  update_vertex_pool();
}

INLINE float LUISprite::get_z_index() {
  return _data[0].y;
}


INLINE void LUISprite::print_vertices() {
  cout << "LUISprite, 4 Vertices:" << endl;

  for (int i = 0; i < 4; i++) {
    cout << "  [Vertex] POS = " << _data[i].x << "," << _data[i].y << "," << _data[i].z 
      << "; UV = " << _data[i].u << "," << _data[i].v 
      << " COL = " << (float)_data[i].color[0] << "," << (float)_data[i].color[1] << "," << (float)_data[i].color[2] << "," << (float)_data[i].color[3] << endl;
  }

}
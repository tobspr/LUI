

INLINE void LUISprite::set_uv_range(const LTexCoord& uv_begin, const LTexCoord& uv_end) {
  set_uv_range(uv_begin.get_x(), uv_begin.get_y(), uv_end.get_x(), uv_end.get_y());
}

INLINE void LUISprite::set_uv_range(float u0, float v0, float u1, float v1) {
  _uv_begin.set(u0, v0);
  _uv_end.set(u1, v1);
}

INLINE const LTexCoord& LUISprite::get_uv_begin() const {
  return _uv_begin;
}

INLINE const LTexCoord& LUISprite::get_uv_end() const {
  return _uv_end;
}

INLINE void LUISprite::set_texture(Texture* tex, bool resize) {
  if (tex == _tex) {
    // No change
    return;
  }

  _texture_index = -1;

  // Unassign old texture
  if (_tex != nullptr) {
    _tex = tex;
    _debug_source = tex->get_name();
  } else {
    _debug_source = "nullptr";
  }

  if (tex != nullptr) {
    if (luiSprite_cat.is_spam()) {
      luiSprite_cat.spam() << "Assigned texture of size " << tex->get_x_size() << "x" << tex->get_y_size() << endl;
    }

    _tex = tex;
    set_uv_range(LTexCoord(0), LTexCoord(1));

    if (resize) {
      set_size(_tex->get_x_size(), _tex->get_y_size());
    }

    // Assign new index
    if (_root != nullptr) {
        fetch_texture_index();
    }
  }
}

INLINE void LUISprite::set_texture(const LUIAtlasDescriptor& descriptor, bool resize) {

  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Load texture data from descriptor" << endl;
  }

  set_texture(descriptor.get_texture(), false);
  set_uv_range(descriptor.get_uv_begin(), descriptor.get_uv_end());

  if (resize) {
    set_size(descriptor.get_size());
  }
}

INLINE void LUISprite::set_texture(const string& source, bool resize) {

  _debug_source = source;
  size_t sep_pos = source.find(":");
  if (sep_pos != string::npos) {

    // load texture from descriptor
    // "atlas-id:entry-name"
    string atlas_id = source.substr(0, sep_pos);
    string entry_name = source.substr(sep_pos+1);
    set_texture(entry_name, atlas_id, resize);

  } else {

    // load texture from file
    PT(Texture) tex = TexturePool::load_texture(source);

    if (tex == nullptr) {
      luiSprite_cat.error() << "Could not load texture from '" << source << "'" << endl;
      return;
    }

    set_texture(tex, resize);
  }
}

INLINE void LUISprite::set_texture(const string& entry_name, const string& atlas_id, bool resize) {
  if (luiSprite_cat.is_spam()) {
    luiSprite_cat.spam() << "Load texture from atlas" << endl;
  }
  _debug_source =  entry_name + ":" + atlas_id;
  set_texture(LUIAtlasPool::get_global_ptr()->get_descriptor(atlas_id, entry_name), resize);
}

INLINE Texture* LUISprite::get_texture() const {
  return _tex;
}

INLINE void LUISprite::print_vertices() {
  cout << "LUISprite, 4 Vertices:" << endl;
  recompute_vertices();
  for (int i = 0; i < 4; i++) {
    cout << "  [Vertex] POS = " << _data[i].x << "," << _data[i].y << "," << _data[i].z
      << "; UV = " << _data[i].u << "," << _data[i].v
      << " COL = " << (float)_data[i].color[0] << "," << (float)_data[i].color[1] << "," << (float)_data[i].color[2] << "," << (float)_data[i].color[3] << endl;
  }
}

INLINE void LUISprite::on_detached() {
  unregister_events();
  if (_tex != nullptr) {
    unassign_sprite_index();
  }
  _root = nullptr;
  _parent = nullptr;
}

INLINE void LUISprite::init_size(float w, float h) {
  if (w > 0.0 && h > 0.0)
    set_size(w, h);
  else if (w > 0.0)
    set_width(w);
  else if (h > 0.0)
    set_height(h);
}

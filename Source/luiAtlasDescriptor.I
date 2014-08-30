

INLINE Texture* LUIAtlasDescriptor::get_texture() const {
  return _tex;
}

INLINE const LVector2 &LUIAtlasDescriptor::get_size() const {
  return _size;
}

INLINE const LVector2 &LUIAtlasDescriptor::get_uv_begin() const {
  return _uv_begin;
}

INLINE const LVector2 &LUIAtlasDescriptor::get_uv_end() const {
  return _uv_end;
}

INLINE void LUIAtlasDescriptor::set_texture(Texture* tex) {
  _tex = tex;
}

INLINE void LUIAtlasDescriptor::set_size(const LVector2 &size) {
  _size = size;
}

INLINE void LUIAtlasDescriptor::set_uv_begin(const LVector2 &uv_begin) {
  _uv_begin = uv_begin;
}

INLINE void LUIAtlasDescriptor::set_uv_end(const LVector2 &uv_end) {
  _uv_end = uv_end;
}
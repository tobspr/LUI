
/**
 * @brief Returns the stored texture
 * @details This returns the texture previously stored with
 *   LUIAtlasDescriptor::set_texture(). Usually this is a handle to the atlas
 *   texture.
 * @return Texture handle, or nullptr if no texture was set
 */
INLINE Texture* LUIAtlasDescriptor::get_texture() const {
  return _tex;
}

/**
 * @brief Returns the size of the sprite
 * @details This returns the size of the referenced sprite in pixels, previously
 *   set with LUIAtlasDescriptor::set_size().
 *
 * @return Texture size
 */
INLINE const LVector2& LUIAtlasDescriptor::get_size() const {
  return _size;
}

/**
 * @brief Returns the uv-start coordinate
 * @details Returns the start of the sprite in atlas space. This is the value
 *   previously set with LUIAtlasDescriptor::set_uv_range().
 *
 * @return uv-start coordinate
 */
INLINE const LTexCoord& LUIAtlasDescriptor::get_uv_begin() const {
  return _uv_begin;
}

/**
 * @brief Returns the uv-end coordinate
 * @details Returns the end of the sprite in atlas space. This is the value
 *   previously set with LUIAtlasDescriptor::set_uv_range().
 *
 * @return uv-end coordinate
 */
INLINE const LTexCoord& LUIAtlasDescriptor::get_uv_end() const {
  return _uv_end;
}

/**
 * @brief Sets the atlas texture
 * @details This sets the handle to the texture. This should only happen while
 *   the descriptor gets created, and only the LUIAtlasPool has access to this
 *   method.
 *
 *   The descriptor will not keep track of the texture, so it is important
 *   to ensure the texture handle stays valid while the descriptor exists.
 *
 * @param tex Handle to the atlas texture.
 */
INLINE void LUIAtlasDescriptor::set_texture(Texture* tex) {
  _tex = tex;
}

/**
 * @brief Sets the size of the contained sprite
 * @details This sets the size of the sprite in pixels. This can be useful at
 *   some places, however it can also be deduced from the uv coordinates
 *   and atlas size.
 *
 * @param size Size of the sprite in pixels
 */
INLINE void LUIAtlasDescriptor::set_size(const LVector2& size) {
  _size = size;
}

/**
 * @brief Sets the uv coordinates
 * @details This sets the uv coordinates of the sprite in atlas space, thus from
 *   (0, 0) to (1, 1). uv_begin should be the upper-left coordinate of the sprite,
 *   and uv_end should be the lower-right one.
 *
 * @param uv_begin Upper left coordinate in uv space
 * @param uv_end Lower right coordinate in uv space
 */
INLINE void LUIAtlasDescriptor::set_uv_range(const LTexCoord& uv_begin, const LTexCoord& uv_end) {
  _uv_begin = uv_begin;
  _uv_end = uv_end;
}

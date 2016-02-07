
/**
 * @brief Checks whether an entry exists in the atlas.
 * @details This methods checks if an entry with the given name exists in the
 *   atlas. If an entry was found, true is returned, otherwise false.
 *
 * @param name Entry name, case sensitive
 * @return true if the entry was found, false otherwise
 */
INLINE bool LUIAtlas::has_entry(const string& name) const {
  return _entries.count(name) != 0;
}

/**
 * @brief Returns an atlas entry.
 * @details This search for an atlas entry with the given name, and returns it.
 *   If an entry was not found in the atlas, an assertion is raised.
 *   This behaviour can be prevented by using LUIAtlas::has_entry() before.
 *
 * @param name Entry name, case sensitive
 * @return Handle to the atlas entry
 */
INLINE const LUIAtlasEntry& LUIAtlas::get_entry(const string& name) const {
  auto it = _entries.find(name);

  if (it == _entries.end()) {
    lui_cat.error() << "Entry '" << name << "' is not present in atlas" << endl;
    nassertr(false, _entries.begin()->second);
  }

  return it->second;
}

/**
 * @brief Returns the atlas texture
 * @details This returns a handle to the atlas texture, which can be used for
 *   rendering.
 * @return Handle to the atlas texture
 */
INLINE Texture* LUIAtlas::get_texture() const {
  return _tex;
}

/**
 * @brief Returns the atlas size.
 * @details Returns the atlas size in pixels, this is a convenience function for
 *   Texture::get_x_size(). It assumes the atlas has the same width and height.
 * @return Size of the atlas in pixels
 */
INLINE int LUIAtlas::get_size() const {
  return _tex->get_x_size();
}

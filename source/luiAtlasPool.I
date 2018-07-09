
/**
 * @brief Checks whether an atlas exists
 * @details This method checks if there was an atlas loaded with the given name.
 *   If this is the case, the method returns true, otherwise false.
 *
 * @param atlas_id Name of the atlas, case sensitive
 * @return true if the atlas was loaded, false otherwise
 */
INLINE bool LUIAtlasPool::has_atlas(const string& atlas_id) const {
  return _atlases.count(atlas_id) > 0;
}

/**
 * @brief Returns an atlas by name
 * @details This method returns an atlas with the given name. If the name was
 *   not found, because the atlas was not loaded yet, null is returned.
 *
 * @param atlas_id Name of the atlas
 * @return Handle to the atlas, or null
 */
INLINE PT(LUIAtlas) LUIAtlasPool::get_atlas(const string& atlas_id) const {
  auto it = _atlases.find(atlas_id);
  if (it != _atlases.end()) {
    return it->second;
  }
  return nullptr;
}

/**
 * @brief Returns a descriptor from a given atlas
 * @details This returns a descriptor with the given name from the given atlas.
 *   If there is no atlas with the given name, or no entry in that in that atlas
 *   exists, an error is printed, and an assertion is raised.
 *
 *   The descriptor contains information about the atlas texture, size, and the
 *   uv position of the referenced sprite.
 *
 * @param atlas_id Name of the atlas
 * @param entry_id Name of the entry
 *
 * @return Descriptor of the sprite
 */
INLINE LUIAtlasDescriptor LUIAtlasPool::get_descriptor(const string& atlas_id, const string& entry_id) const {
  if (!has_atlas(atlas_id)) {
    lui_cat.error() << "Atlas '" << atlas_id << "' not found!" << endl;
    nassertr(false, LUIAtlasDescriptor());
  }

  LUIAtlas* atlas = get_atlas(atlas_id);
  const LUIAtlasEntry& entry = atlas->get_entry(entry_id);

  LUIAtlasDescriptor descriptor;
  descriptor.set_size(entry.size);
  descriptor.set_uv_range(
      entry.pos / float(atlas->get_size()),
      (entry.pos + entry.size) / float(atlas->get_size()) );
  descriptor.set_texture(atlas->get_texture());
  return descriptor;
}

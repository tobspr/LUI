

INLINE bool LUIAtlas::has_entry(const string &name) {
  return _entries.count(name) != 0;
}

INLINE LUIAtlasEntry* LUIAtlas::get_entry(const string &name) {
  if (has_entry(name))
    return _entries[name];

  lui_cat.error() << "Entry '" << name << "' is not present in atlas" << endl;
  return NULL;
}

INLINE Texture* LUIAtlas::get_texture() {
  return _tex;
}

INLINE int LUIAtlas::get_size() {
  return _size;
}
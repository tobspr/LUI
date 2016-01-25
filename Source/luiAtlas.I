

INLINE bool LUIAtlas::has_entry(const string &name) const {
  return _entries.count(name) != 0;
}

INLINE LUIAtlasEntry* LUIAtlas::get_entry(const string &name) const {
  auto it = _entries.find(name);
  if (it != _entries.end())
    return it->second;

  lui_cat.error() << "Entry '" << name << "' is not present in atlas" << endl;
  return NULL;
}

INLINE Texture* LUIAtlas::get_texture() const {
  return _tex;
}

INLINE int LUIAtlas::get_size() const {
  return _size;
}

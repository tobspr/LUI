

INLINE bool LUIFontPool::has_font(const string &name) {
  return _fonts.count(name) == 1;
}

DynamicTextFont* LUIFontPool::get_font(const string &name) {
  nassertr(has_font(name), NULL);
  return _fonts[name];
}
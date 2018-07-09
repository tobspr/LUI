

INLINE bool LUIFontPool::has_font(const string& name) const {
  return _fonts.count(name) == 1;
}

DynamicTextFont* LUIFontPool::get_font(const string& name) const {
  nassertr(has_font(name), nullptr);
  return _fonts.at(name);
}


INLINE void LUIText::set_font(const string& font_name) {
    _font = LUIFontPool::get_global_ptr()->get_font(font_name);
    update_text();
}

INLINE void LUIText::set_text(const wstring& text) {
    if (_text != text) {
        _text = text;
        update_text();
    }
}

INLINE void LUIText::set_font_size(float size) {
  if (size != _font_size) {
    _font_size = size;
    update_text();
  }
}

INLINE DynamicTextFont* LUIText::get_font() const{
    return _font;
}

INLINE const wstring& LUIText::get_text() const {
    return _text;
}

INLINE float LUIText::get_font_size() const {
    return _font_size;
}

INLINE void LUIText::set_wordwrap(bool wrap) {
  _wordwrap = wrap;
  update_text();
}

INLINE bool LUIText::get_wordwrap() const {
  return _wordwrap;
}


INLINE void LUIText::set_font(const string &font_name) {
    _font = LUIFontPool::get_global_ptr()->get_font(font_name);
    update_text();
}

INLINE void LUIText::set_text(const string &text) {
    if (_text.compare(text) != 0) {
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
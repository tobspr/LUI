

#include "luiFontPool.h"


LUIFontPool* LUIFontPool::_global_ptr = nullptr;

LUIFontPool::LUIFontPool() {

  PT(DynamicTextFont) font = DCAST(DynamicTextFont,  TextProperties::get_default_font());
  if (font != nullptr) {
    register_font("default", font);
  } else {
    lui_cat.warning() << "Could not load default font, as it is no dynamic font!" << endl;
  }

}

LUIFontPool::~LUIFontPool() {
}

LUIFontPool* LUIFontPool::get_global_ptr() {
  if (_global_ptr == nullptr) {
    _global_ptr = new LUIFontPool();
  }
  return _global_ptr;
}

void LUIFontPool::register_font(const string& name, PT(DynamicTextFont) font) {
  _fonts[name] = font;
  if (font->get_num_pages() > 0) {
    lui_cat.warning() << "Font was already used, calling clear() first." << endl;
    font->clear();
  }
  font->set_fg(LColor(0.99, 0.99, 0.99, 1.0));
}

void LUIFontPool::load_font(const string& name, const string&font_file) {
  lui_cat.error() << "Todo: LUIFontPool::load_font" << endl;
}



#include "luiFontPool.h"


LUIFontPool *LUIFontPool::_global_ptr = NULL;

LUIFontPool::LUIFontPool() {

  PT(DynamicTextFont) font = DCAST(DynamicTextFont,  TextProperties::get_default_font());
  if (font != NULL) {
    register_font("default", font);
  } else {
    lui_cat.warning() << "Could not load default font, as it is no dynamic font!" << endl;
  }

}

LUIFontPool::~LUIFontPool() {

}

LUIFontPool* LUIFontPool::get_global_ptr() {
  if (_global_ptr == (LUIFontPool *)NULL) {
    _global_ptr = new LUIFontPool();
  }
  return _global_ptr;
}

void LUIFontPool::register_font(const string &name, PT(DynamicTextFont) font) {
  lui_cat.debug() << "Registering font " << name << endl;
  // Fonts should be white, so the color scale works properly
  font->set_fg(LVecBase4f(0.99,0.99,0.99,1));


  _fonts[name] = font;
}


void LUIFontPool::load_font(const string &name, const string&font_file) {
  lui_cat.error() << "Todo: LUIFontPool::load_font" << endl;
}

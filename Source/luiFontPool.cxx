

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
  _fonts[name] = font;
}
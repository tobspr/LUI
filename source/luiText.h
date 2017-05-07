// Filename: luiText.h
// Created by:  tobspr (14Sep14)
//

#ifndef LUI_TEXT_H
#define LUI_TEXT_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "config_lui.h"
#include "luiObject.h"
#include "luiIterators.h"
#include "luiFontPool.h"
#include "luiColorable.h"
#include "luiSprite.h"
#include "dynamicTextFont.h"
#include "dynamicTextGlyph.h"
#include "textFont.h"
#include "texture.h"
#include "dcast.h"

class EXPCL_LUI LUIText : public LUIObject {

PUBLISHED:

  LUIText(PyObject* self,
    LUIObject* parent, const wstring& text, const string& font_name="default",
    float font_size=16.0f, float x=0.0f, float y=0.0f, bool wordwrap=false);
  ~LUIText();

  INLINE void set_font(const string& font_name);
  INLINE DynamicTextFont* get_font() const;

  INLINE void set_text(const wstring& text);
  INLINE const wstring& get_text() const;

  INLINE void set_font_size(float size);
  INLINE float get_font_size() const;

  INLINE void set_wordwrap(bool wrap);
  INLINE bool get_wordwrap() const;

  int get_char_index(float pos) const;
  float get_char_pos(int char_index) const;

  virtual void ls(int indent = 0);

  MAKE_PROPERTY(font, get_font, set_font);
  MAKE_PROPERTY(text, get_text, set_text);
  MAKE_PROPERTY(font_size, get_font_size, set_font_size);

protected:

  void update_text();
  vector<int> get_line_breaks();

  DynamicTextFont* _font;
  wstring _text;
  float _font_size;
  bool _wordwrap;
  pvector<CPT(DynamicTextGlyph)> _glyphs;


public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LUIObject::init_type();
    register_type(_type_handle, "LUIText", LUIObject::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;


};

#include "luiText.I"

#endif

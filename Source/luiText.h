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
#include "luiFontPool.h"
#include "luiSprite.h"
#include "dynamicTextFont.h"
#include "dynamicTextGlyph.h"
#include "textFont.h"
#include "texture.h"
#include "dcast.h"

class EXPCL_PANDASKEL LUIText : public LUIObject {

PUBLISHED:

  LUIText(float x = 0.0, float y = 0.0);
  LUIText(LUIObject *parent, float x = 0.0, float y = 0.0);
  LUIText(LUIObject *parent, const string &text, const string &font_name = "default", float x = 0.0, float y = 0.0);

  ~LUIText();

  INLINE void set_font(const string &font_name);
  INLINE void set_text(const string &text);
  INLINE void set_font_size(float size);

protected:

  void update_text();

  DynamicTextFont *_font;
  string _text;
  float _font_size;
  pvector<PT(DynamicTextGlyph)> _glyphs;

};

#include "luiText.I"

#endif
// Filename: luiFontPool.h
// Created by:  tobspr (13Sep14)
//

#ifndef LUI_FONT_POOL_H
#define LUI_FONT_POOL_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "filename.h"
#include "dynamicTextFont.h"
#include "textProperties.h"
#include "dcast.h"
#include "config_lui.h"

class EXPCL_LUI LUIFontPool {

PUBLISHED:

  static LUIFontPool* get_global_ptr();
  void load_font(const string& name, const string&font_file);
  void register_font(const string& name, PT(DynamicTextFont) font);
  INLINE bool has_font(const string& name) const;
  INLINE DynamicTextFont* get_font(const string& name) const;

private:

  LUIFontPool();
  ~LUIFontPool();

  pmap<string, PT(DynamicTextFont)> _fonts;

  static LUIFontPool* _global_ptr;

};

#include "luiFontPool.I"

#endif

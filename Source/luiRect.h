// Filename: luiRect.h
// Created by:  tobspr (22Sep14)
//

#ifndef LUI_RECT_H
#define LUI_RECT_H

#include "config_lui.h"
#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"

class EXPCL_LUI LUIRect : public ReferenceCount {

PUBLISHED:

  LUIRect(const LVector4 &rect);
  LUIRect(float x, float y, float w, float h);
  ~LUIRect();

  INLINE float get_x();
  INLINE float get_y();
  INLINE float get_w();
  INLINE float get_h();

  INLINE void set_x(float x);
  INLINE void set_y(float y);
  INLINE void set_w(float w);
  INLINE void set_h(float h);

  INLINE void set_rect(const LVector4 &rect);
  INLINE void set_rect(float x, float y, float w, float h);

  INLINE const LVector4 &get_rect();

  MAKE_PROPERTY(x, get_x, set_x);
  MAKE_PROPERTY(y, get_y, set_y);
  MAKE_PROPERTY(w, get_w, set_w);
  MAKE_PROPERTY(h, get_h, set_h);

protected:

  LVector4 _rect;

};

#include "luiRect.I"

#endif

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

class EXPCL_LUI LUIRect {

PUBLISHED:
  LUIRect() : _rect(-1) {};
  explicit LUIRect(const LVector4& rect) : _rect(rect) {};
  LUIRect(float x, float y, float w, float h) : _rect(x, y, w, h) {};

  INLINE float get_x() const;
  INLINE float get_y() const;
  INLINE float get_w() const;
  INLINE float get_h() const;

  INLINE LVector2 get_xy() const;
  INLINE LVector2 get_wh() const;

  INLINE void set_x(float x);
  INLINE void set_y(float y);
  INLINE void set_w(float w);
  INLINE void set_h(float h);

  INLINE void set_rect(const LVector4& rect);
  INLINE void set_rect(const LVector2& xy, const LVector2& wh);
  INLINE void set_rect(float x, float y, float w, float h);


  INLINE const LVector4& get_rect() const;

  MAKE_PROPERTY(x, get_x, set_x);
  MAKE_PROPERTY(y, get_y, set_y);
  MAKE_PROPERTY(w, get_w, set_w);
  MAKE_PROPERTY(h, get_h, set_h);

  friend ostream& operator<<(ostream& stream, const LUIRect& rect) {
    return stream << "Rect[" << rect.get_x() << " x " << rect.get_y() << " / "
                  << rect.get_w() << " x " << rect.get_h() << "]";
  }

protected:
  LVector4 _rect;
};


INLINE bool operator==(const LUIRect& a, const LUIRect& b) { return a.get_rect() == b.get_rect(); }
INLINE bool operator!=(const LUIRect& a, const LUIRect& b) { return !(a == b); }

#include "luiRect.I"

#endif

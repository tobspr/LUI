// Filename: luiBounds.h
// Created by:  tobspr (20Sep14)
//

#ifndef LUI_BOUNDS_H
#define LUI_BOUNDS_H

#include "config_lui.h"
#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"

class EXPCL_LUI LUIBounds {

PUBLISHED:

  LUIBounds() : _bounds(-1) {};
  explicit LUIBounds(float fill_value) : _bounds(fill_value) {};
  explicit LUIBounds(const LVector4& bounds) : _bounds(bounds) {};
  LUIBounds(float top, float right, float bottom, float left)
    : _bounds(top, right, bottom, left) {};

  INLINE float get_top() const;
  INLINE float get_right() const;
  INLINE float get_bottom() const;
  INLINE float get_left() const;

  INLINE void set_top(float top);
  INLINE void set_right(float right);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);

  INLINE void set_bounds(const LVector4& bounds);
  INLINE void set_bounds(float top, float right, float bottom, float left);

  INLINE const LVector4& get_bounds() const;

  MAKE_PROPERTY(top, get_top, set_top);
  MAKE_PROPERTY(right, get_right, set_right);
  MAKE_PROPERTY(bottom, get_bottom, set_bottom);
  MAKE_PROPERTY(left, get_left, set_left);

  friend ostream& operator<<(ostream& stream, const LUIBounds& bounds) {
    return stream << "Bounds[" << bounds.get_top() << ", " << bounds.get_right() << ", "
                  << bounds.get_bottom() << ", " << bounds.get_left() << "]";
  }
protected:

  LVector4 _bounds;
};


INLINE bool operator==(const LUIBounds& a, const LUIBounds& b) { return a.get_bounds() == b.get_bounds(); }
INLINE bool operator!=(const LUIBounds& a, const LUIBounds& b) { return !(a == b); }


#include "luiBounds.I"

#endif

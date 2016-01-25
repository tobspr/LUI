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

class EXPCL_LUI LUIBounds : public ReferenceCount {

PUBLISHED:

  LUIBounds(const LVector4 &bounds);
  LUIBounds(float top, float right, float bottom, float left);
  ~LUIBounds();

  INLINE float get_top();
  INLINE float get_right();
  INLINE float get_bottom();
  INLINE float get_left();



  INLINE void set_bounds(const LVector4 &bounds);
  INLINE void set_bounds(float top, float right, float bottom, float left);

  INLINE const LVector4 &get_bounds();

  MAKE_PROPERTY(top, get_top);
  MAKE_PROPERTY(bottom, get_bottom);
  MAKE_PROPERTY(left, get_left);
  MAKE_PROPERTY(right, get_right);

public:

  INLINE void set_top(float top);
  INLINE void set_right(float right);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);

protected:

  LVector4 _bounds;

};

#include "luiBounds.I"

#endif

// Filename: luiColorable.h
// Created by:  tobspr (19Sep14)
//

#ifndef LUI_COLORABLE_H
#define LUI_COLORABLE_H

#include "config_lui.h"
#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"

class EXPCL_LUI LUIColorable {

PUBLISHED:

  // Color
  INLINE void set_color(const LColor& color);
  INLINE void set_color(const LVecBase3& rgb);
  INLINE void set_color(float r, float g, float b, float a = 1.0);

  INLINE void set_red(float r);
  INLINE void set_green(float g);
  INLINE void set_blue(float b);
  INLINE void set_alpha(float a);

  INLINE float get_red() const;
  INLINE float get_green() const;
  INLINE float get_blue() const;
  INLINE float get_alpha() const;

  INLINE const LColor& get_color() const;
  INLINE const LColor& get_composed_color() const;

  // Python properties
  MAKE_PROPERTY(color, get_color, set_color);
  MAKE_PROPERTY(composed_color, get_composed_color);
  MAKE_PROPERTY(red, get_red, set_red);
  MAKE_PROPERTY(green, get_green, set_green);
  MAKE_PROPERTY(blue, get_blue, set_blue);
  MAKE_PROPERTY(alpha, get_alpha, set_alpha);

protected:

  LUIColorable();
  virtual ~LUIColorable();

  INLINE void compose_color(const LColor& parent_color = LColor(1));

  LColor _color;
  LColor _composed_color;
};

#include "luiColorable.I"

#endif

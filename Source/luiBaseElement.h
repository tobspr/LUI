// Filename: luiBaseElement.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_BASE_ELEMENT_H
#define LUI_BASE_ELEMENT_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "config_lui.h"

class LUIRoot;

class EXPCL_PANDASKEL LUIBaseElement {



PUBLISHED:

  LUIBaseElement();
  virtual ~LUIBaseElement();

  // Position
  INLINE void set_top_left(float top, float left);
  INLINE void set_pos(float top, float left);

  INLINE void set_top(float top);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);
  INLINE void set_right(float right);
  INLINE LVector2 get_abs_pos();

  // Size
  INLINE void set_size(const LVector2 &size);
  INLINE void set_size(float w, float h);
  INLINE void set_width(float w);
  INLINE void set_height(float h);
  INLINE float get_width();
  INLINE float get_height();
  INLINE const LVector2 &get_size() const;

  // Visible
  INLINE void set_visible(bool visible);
  INLINE bool is_visible();
  INLINE void hide();
  INLINE void show();

  INLINE LUIBaseElement* get_parent();

public:

  INLINE void set_parent(LUIBaseElement* parent);
  void recompute_position();

protected:

  virtual void set_root(LUIRoot* root) = 0;
  virtual void on_detached() = 0;

  // Interface
  virtual void on_bounds_changed() = 0;
  virtual void on_visibility_changed() = 0;

  PN_stdfloat _offset_x, _offset_y;
  bool _stick_top, _stick_left;
  PN_stdfloat _pos_x, _pos_y;
  LVector2 _size;
  bool _visible;

  LUIBaseElement *_parent;
  LUIRoot *_root;

};

#include "luiBaseElement.I"

#endif
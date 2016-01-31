// Filename: luiBaseElement.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_BASE_ELEMENT_H
#define LUI_BASE_ELEMENT_H

#include "config_lui.h"
#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "callbackObject.h"
#include "luiColorable.h"
#include "luiBounds.h"
#include "luiRect.h"
#include "luiExpression.h"

#include <unordered_map>

typedef struct _object PyObject;

class LUIRoot;
class LUIObject;
class LUIRect;

NotifyCategoryDecl(luiBaseElement, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIBaseElement : public TypedReferenceCount, public LUIColorable {

  friend class LUIObject;
  friend class LUIText;

PUBLISHED:
  LUIBaseElement(PyObject *self);
  virtual ~LUIBaseElement();

  // Events
  INLINE void bind(const string &event_name, CallbackObject* callback);
  INLINE void unbind(const string &event_name);
  INLINE void unbind_all();

  INLINE bool has_event(const string &event_name);
  void trigger_event(const string &event_name, const wstring &message = wstring(), const LPoint2 &coords = LPoint2(0));

  // Position
  INLINE void set_left_top(const LPoint2 &pos);
  INLINE void set_right_top(const LPoint2 &pos);
  INLINE void set_left_bottom(const LPoint2 &pos);
  INLINE void set_right_bottom(const LPoint2 &pos);

  INLINE LPoint2 get_left_top() const;
  INLINE LPoint2 get_right_top() const;
  INLINE LPoint2 get_left_bottom() const;
  INLINE LPoint2 get_right_bottom() const;

  INLINE void set_pos(const LPoint2 &pos);
  INLINE void set_pos(float x, float y);
  INLINE LPoint2 get_pos() const;

  INLINE LPoint2 get_abs_pos() const;

  INLINE void set_top(float top);
  INLINE void set_right(float right);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);

  INLINE float get_top() const;
  INLINE float get_right() const;
  INLINE float get_bottom() const;
  INLINE float get_left() const;

  INLINE LPoint2 get_relative_pos(const LPoint2 &abs_pos) const;

  INLINE void set_centered(bool center_vert = true, bool center_horiz = true);
  INLINE void set_center_vertical(bool centered = true);
  INLINE void set_center_horizontal(bool centered = true);

  INLINE bool is_centered() const;
  INLINE bool is_vertical_centered() const;
  INLINE bool is_horizontal_centered() const;

  // Margin
  INLINE void set_margin(const LVector4 &margin);
  INLINE void set_margin(float top, float right, float bottom, float left);
  INLINE void set_margin(float margin);
  INLINE void set_margin_top(float top);
  INLINE void set_margin_right(float right);
  INLINE void set_margin_bottom(float bottom);
  INLINE void set_margin_left(float left);
  INLINE float get_margin_top() const;
  INLINE float get_margin_right() const;
  INLINE float get_margin_bottom() const;
  INLINE float get_margin_left() const;
  INLINE const LUIBounds& get_margin() const;

  // Padding
  INLINE void set_padding(const LVector4 &padding);
  INLINE void set_padding(float top, float right, float bottom, float left);
  INLINE void set_padding(float padding);
  INLINE void set_padding_top(float top);
  INLINE void set_padding_right(float right);
  INLINE void set_padding_bottom(float bottom);
  INLINE void set_padding_left(float left);
  INLINE float get_padding_top() const;
  INLINE float get_padding_right() const;
  INLINE float get_padding_bottom() const;
  INLINE float get_padding_left() const;
  INLINE const LUIBounds& get_padding() const;

  // Size
  INLINE void set_size(const LVector2 &size);
  INLINE void set_size(float w, float h);
  INLINE void set_width(float w);
  INLINE void set_height(float h);
  INLINE float get_width() const;
  INLINE float get_height() const;
  INLINE bool has_size() const;
  INLINE const LVector2& get_size() const;

  // Visible
  INLINE void set_visible(bool visible);
  INLINE bool is_visible() const;
  INLINE void hide();
  INLINE void show();

  // Solid
  INLINE void set_solid(bool solid);
  INLINE bool get_solid() const;

  // Z-Index
  void set_z_offset(int z_offset);
  INLINE float get_z_offset() const;

  // Focus
  INLINE bool has_focus() const;
  void request_focus();
  void blur();

  INLINE bool has_parent() const;
  void clear_parent();
  void set_parent(LUIObject *parent);
  INLINE LUIObject* get_parent() const;

  INLINE virtual bool intersects(float x, float y) const;

  INLINE void begin_update_section();
  INLINE virtual void end_update_section();

  INLINE void clear_clip_bounds();
  INLINE void set_clip_bounds(const LUIBounds& bounds);
  INLINE void set_clip_bounds(float top, float right, float bottom, float left);
  INLINE const LUIBounds& get_clip_bounds() const;
  INLINE const LUIRect& get_abs_clip_bounds() const;

  INLINE bool is_topmost() const;
  INLINE void set_topmost(bool topmost);

  INLINE void set_emits_changed_event(bool emit);
  INLINE bool get_emits_changed_event() const;

  INLINE float get_x_extent();
  INLINE float get_y_extent();

  INLINE float get_inner_width();
  INLINE float get_inner_height();

  // Properties for python
  MAKE_PROPERTY(left_top, get_left_top, set_left_top);
  MAKE_PROPERTY(right_top, get_right_top, set_right_top);
  MAKE_PROPERTY(left_bottom, get_left_bottom, set_left_bottom);
  MAKE_PROPERTY(right_bottom, get_right_bottom, set_right_bottom);

  MAKE_PROPERTY(pos, get_pos, set_pos);
  MAKE_PROPERTY(abs_pos, get_abs_pos);

  MAKE_PROPERTY(top, get_top, set_top);
  MAKE_PROPERTY(bottom, get_bottom, set_bottom);
  MAKE_PROPERTY(left, get_left, set_left);
  MAKE_PROPERTY(right, get_right, set_right);

  MAKE_PROPERTY(centered, is_centered, set_centered);
  MAKE_PROPERTY(center_vertical, is_vertical_centered, set_center_vertical);
  MAKE_PROPERTY(center_horizontal, is_horizontal_centered, set_center_horizontal);

  MAKE_PROPERTY(margin, get_margin, set_margin);
  MAKE_PROPERTY(margin_top, get_margin_top, set_margin_top);
  MAKE_PROPERTY(margin_right, get_margin_right, set_margin_right);
  MAKE_PROPERTY(margin_bottom, get_margin_bottom, set_margin_bottom);
  MAKE_PROPERTY(margin_left, get_margin_left, set_margin_left);

  MAKE_PROPERTY(padding, get_padding, set_padding);
  MAKE_PROPERTY(padding_top, get_padding_top, set_padding_top);
  MAKE_PROPERTY(padding_right, get_padding_right, set_padding_right);
  MAKE_PROPERTY(padding_bottom, get_padding_bottom, set_padding_bottom);
  MAKE_PROPERTY(padding_left, get_padding_left, set_padding_left);

  MAKE_PROPERTY(size, get_size, set_size);
  MAKE_PROPERTY(width, get_width, set_width);
  MAKE_PROPERTY(height, get_height, set_height);

  MAKE_PROPERTY(visible, is_visible, set_visible);
  MAKE_PROPERTY(z_offset, get_z_offset, set_z_offset);
  MAKE_PROPERTY(absolute_z_offset, get_abs_pos);
  MAKE_PROPERTY(focused, has_focus);
  MAKE_PROPERTY2(parent, has_parent, get_parent, set_parent, clear_parent);

  MAKE_PROPERTY(clip_bounds, get_clip_bounds, set_clip_bounds);
  MAKE_PROPERTY(topmost, is_topmost, set_topmost);
  MAKE_PROPERTY(solid, get_solid, set_solid);

  MAKE_PROPERTY(emits_changed_event, get_emits_changed_event, set_emits_changed_event);

  MAKE_PROPERTY(x_extent, get_x_extent);
  MAKE_PROPERTY(y_extent, get_y_extent);

  MAKE_PROPERTY(inner_width, get_inner_width);
  MAKE_PROPERTY(inner_height, get_inner_height);

public:

  INLINE void do_set_parent(LUIObject* parent);
  void recompute_position();

  INLINE void set_snap_position(bool snap);

  virtual void ls(int ident = 0) = 0;

  INLINE void set_focus(bool focus);
  INLINE int get_last_frame_visible() const;
  INLINE int get_last_render_index() const;

  INLINE void do_set_z_offset(int z_offset);

  INLINE bool contributes_to_fluid_width() const;
  INLINE bool contributes_to_fluid_height() const;

  virtual void update_dimensions();


protected:

  float get_parent_width() const;
  float get_parent_height() const;

  void fetch_render_index();

  enum LUIPlacementMode {

    // Stick to left
    M_default,

    // Stick to right
    M_inverse,

    // Center (either horizontally or vertically)
    M_center
  };

  // Interface
  virtual void set_root(LUIRoot* root) = 0;
  virtual void on_detached() = 0;
  virtual void on_bounds_changed() = 0;

  // Interface to LUIColorable
  virtual void on_color_changed();

  virtual void render_recursive(bool is_topmost_pass, bool render_anyway) = 0;

  void register_events();
  void unregister_events();

  PN_stdfloat _offset_x, _offset_y;
  LUIPlacementMode _placement_x, _placement_y;
  PN_stdfloat _pos_x, _pos_y;
  PN_stdfloat _rel_pos_x, _rel_pos_y;

  LUIExpression _size_x;
  LUIExpression _size_y;
  LVector2 _effective_size;

  bool _visible;
  bool _emits_changed_event;

  // Z-Index, relative to the parent
  float _z_offset;

  // Wheter we already registered the element at the LUIRoot for recieving events
  bool _events_registered;
  bool _in_update_section;
  bool _snap_position;
  bool _focused;
  bool _solid;

  // Margin & Padding, relative to the element bounds
  LUIBounds _margin;
  LUIBounds _padding;

  // Clip bounds, relative to the element bounds
  LUIBounds _clip_bounds;
  bool _have_clip_bounds;

  // Clip bounds, in render space (absolute coordinates)
  LUIRect _abs_clip_bounds;

  unordered_map<string, PT(CallbackObject)> _events;

  LUIRect _last_bounds;
  LUIRect _last_clip_bounds;

  LUIObject* _parent;
  LUIRoot* _root;

  int _last_frame_visible;
  int _last_render_index;
  bool _topmost;


public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "LUIBaseElement", TypedReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;



};

#include "luiBaseElement.I"

#endif

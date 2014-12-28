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
#include "pythonCallbackObject.h"
#include "luiEventData.h"
#include "luiColorable.h"
#include "luiBounds.h"
#include "luiRect.h"

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
  INLINE void bind(const string &event_name, PyObject* callback);
  INLINE void bind(const string &event_name, CallbackObject* callback);
  INLINE void unbind(const string &event_name);
  INLINE void unbind_all();
  INLINE bool has_event(const string &event_name);
  INLINE void trigger_event(const string &event_name, const wstring &message = wstring(), const LPoint2 &coords = LPoint2(0));

  // Position
  INLINE void set_left_top(const LPoint2 &pos);
  INLINE void set_right_top(const LPoint2 &pos);
  INLINE void set_left_bottom(const LPoint2 &pos);
  INLINE void set_right_bottom(const LPoint2 &pos);

  INLINE LPoint2 get_left_top();
  INLINE LPoint2 get_right_top();
  INLINE LPoint2 get_left_bottom();
  INLINE LPoint2 get_right_bottom();

  INLINE void set_pos(const LPoint2 &pos);
  INLINE void set_pos(float x, float y);
  INLINE LPoint2 get_pos();

  INLINE LPoint2 get_abs_pos();

  INLINE void set_top(float top);
  INLINE void set_right(float right);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);

  INLINE float get_top();
  INLINE float get_right();
  INLINE float get_bottom();
  INLINE float get_left();

  INLINE LPoint2 get_relative_pos(const LPoint2 &abs_pos);

  INLINE void set_centered(bool center_vert = true, bool center_horiz = true);
  INLINE void set_center_vertical(bool centered = true);
  INLINE void set_center_horizontal(bool centered = true);

  INLINE bool is_centered();
  INLINE bool is_vertical_centered();
  INLINE bool is_horizontal_centered();


  // Margin
  INLINE void set_margin(const LVector4 &margin);
  INLINE void set_margin(float top, float right, float bottom, float left);
  INLINE void set_margin_top(float top);
  INLINE void set_margin_right(float right);
  INLINE void set_margin_bottom(float bottom);
  INLINE void set_margin_left(float left);
  INLINE float get_margin_top();
  INLINE float get_margin_right();
  INLINE float get_margin_bottom();
  INLINE float get_margin_left();
  INLINE LUIBounds *get_margin();

  // Padding
  INLINE void set_padding(const LVector4 &padding);
  INLINE void set_padding(float top, float right, float bottom, float left);
  INLINE void set_padding_top(float top);
  INLINE void set_padding_right(float right);
  INLINE void set_padding_bottom(float bottom);
  INLINE void set_padding_left(float left);
  INLINE float get_padding_top();
  INLINE float get_padding_right();
  INLINE float get_padding_bottom();
  INLINE float get_padding_left();
  INLINE LUIBounds *get_padding();

  // Size
  INLINE void set_size(const LVector2 &size);
  INLINE void set_size(float w, float h);
  INLINE void set_width(float w);
  INLINE void set_height(float h);
  INLINE float get_width();
  INLINE float get_height();
  INLINE bool has_size();
  INLINE const LVector2 &get_size() const;

  // Visible
  INLINE void set_visible(bool visible);
  INLINE bool is_visible();
  INLINE void hide();
  INLINE void show();

  // Z-Index
  INLINE void set_z_offset(int z_offset);
  INLINE float get_z_offset();

  // Focus
  INLINE bool has_focus();
  void request_focus();
  void blur();

  void reparent_to(LUIBaseElement *parent);
  INLINE LUIBaseElement* get_parent();

  INLINE virtual bool intersects(float x, float y);

  INLINE void begin_update_section();
  INLINE virtual void end_update_section();

  INLINE void set_clip_bounds(LUIBounds *bounds);
  INLINE void set_clip_bounds(float top, float right, float bottom, float left);
  INLINE LUIBounds *get_clip_bounds();
  INLINE LUIRect *get_abs_clip_bounds();

  INLINE bool is_topmost();
  INLINE void set_topmost(bool topmost);

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
  MAKE_PROPERTY(focus, has_focus, request_focus);
  MAKE_PROPERTY(parent, get_parent, reparent_to);

  MAKE_PROPERTY(clip_bounds, get_clip_bounds, set_clip_bounds);
  MAKE_PROPERTY(topmost, is_topmost, set_topmost);


public:

  INLINE void set_parent(LUIBaseElement* parent);
  void recompute_position();

  INLINE void set_snap_position(bool snap);

  virtual void ls(int ident = 0) = 0;

  INLINE void set_focus(bool focus);
  INLINE int get_last_frame_visible();
  INLINE int get_last_render_index();

protected:

  INLINE float get_parent_width();
  INLINE float get_parent_height();

  void fetch_render_index();


  enum LUIPlacementMode {

    // E.g. stick to left
    M_default,

    // E.g. stick to right
    M_inverse,

    // E.g. center horizontally
    M_center
  };

  // Interface
  virtual void set_root(LUIRoot* root) = 0;
  virtual void on_detached() = 0;
  virtual void on_bounds_changed() = 0;
  virtual void on_visibility_changed() = 0;

  // Interface to LUIColorable
  INLINE virtual void on_color_changed();


  virtual void render_recursive(bool is_topmost_pass, bool render_anyway) = 0;

  void register_events();
  void unregister_events();

  PN_stdfloat _offset_x, _offset_y;
  LUIPlacementMode _placement_x, _placement_y;
  PN_stdfloat _pos_x, _pos_y;
  PN_stdfloat _rel_pos_x, _rel_pos_y;
  LVector2 _size;
  bool _visible;

  // Z-Index, relative to the parent
  float _z_offset;

  // Wheter we already registered the element at the LUIRoot for recieving events
  bool _events_registered;

  bool _in_update_section;
  bool _snap_position;

  bool _focused;

  // Margin & Padding, relative to the element bounds
  PT(LUIBounds) _margin;
  PT(LUIBounds) _padding;

  // Clip bounds, relative to the element bounds
  PT(LUIBounds) _clip_bounds;

  // Clip bounds, in render space (absolute coordinates)
  PT(LUIRect)   _abs_clip_bounds;

  pmap<string, PT(CallbackObject)> _events;

  LUIBaseElement *_parent;
  LUIRoot *_root;

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
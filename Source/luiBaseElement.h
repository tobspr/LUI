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


class LUIRoot;
class LUIObject;

NotifyCategoryDecl(luiBaseElement, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIBaseElement : public TypedReferenceCount, public LUIColorable {

  friend class LUIObject;

PUBLISHED:

  LUIBaseElement(PyObject *self);
  virtual ~LUIBaseElement();

  // Events
  INLINE void bind(const string &event_name, PyObject* callback);
  INLINE void bind(const string &event_name, CallbackObject* callback);
  INLINE void unbind(const string &event_name);
  INLINE void unbind_all();
  INLINE bool has_event(const string &event_name);
  INLINE void trigger_event(const string &event_name, const string &message = string(), const LPoint2 &coords = LPoint2(0));

  // Position
  INLINE void set_left_top(const LVector2 &pos);
  INLINE void set_right_top(const LVector2 &pos);
  INLINE void set_left_bottom(const LVector2 &pos);
  INLINE void set_right_bottom(const LVector2 &pos);

  INLINE LVector2 get_left_top();
  INLINE LVector2 get_right_top();
  INLINE LVector2 get_left_bottom();
  INLINE LVector2 get_right_bottom();

  INLINE void set_pos(const LVector2 &pos);
  INLINE void set_pos(float x, float y);
  INLINE LVector2 get_pos();

  INLINE LVector2 get_abs_pos();

  INLINE void set_top(float top);
  INLINE void set_right(float right);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);

  INLINE float get_top();
  INLINE float get_right();
  INLINE float get_bottom();
  INLINE float get_left();

  INLINE void set_centered(bool center_vert = true, bool center_horiz = true);
  INLINE void set_center_vertical(bool centered = true);
  INLINE void set_center_horizontal(bool centered = true);

  INLINE bool is_centered();
  INLINE bool is_vertical_centered();
  INLINE bool is_horizontal_centered();

  // Margin
  INLINE void set_margin(const LVector4 &margin);
  INLINE void set_margin(float top, float right, float bottom, float left);
  INLINE LUIBounds *get_margin();

  // Padding
  INLINE void set_padding(const LVector4 &padding);
  INLINE void set_padding(float top, float right, float bottom, float left);
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
  INLINE float get_abs_z_offset();

  void reparent_to(LUIBaseElement *parent);
  INLINE LUIBaseElement* get_parent();

  INLINE virtual bool intersects(float x, float y);

  INLINE void begin_update_section();
  INLINE virtual void end_update_section();


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
  MAKE_PROPERTY(padding, get_padding, set_padding);
  
  MAKE_PROPERTY(size, get_size, set_size);
  MAKE_PROPERTY(width, get_width, set_width);
  MAKE_PROPERTY(height, get_height, set_height);
  
  MAKE_PROPERTY(visible, is_visible, set_visible);
  MAKE_PROPERTY(z_offset, get_z_offset, set_z_offset);
  MAKE_PROPERTY(absolute_z_offset, get_abs_pos);
  MAKE_PROPERTY(parent, get_parent, reparent_to);

public:

  INLINE void set_parent(LUIBaseElement* parent);
  void recompute_position();

  INLINE void set_snap_position(bool snap);

  virtual void ls(int ident = 0) = 0;

protected:

  INLINE float get_parent_width();
  INLINE float get_parent_height();


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
  virtual void on_z_index_changed() = 0;

  // Interface to LUIColorable
  INLINE virtual void on_color_changed();

  INLINE void recompute_z_index();
  void register_events();
  void unregister_events();

  PN_stdfloat _offset_x, _offset_y;
  LUIPlacementMode _placement_x, _placement_y;
  PN_stdfloat _pos_x, _pos_y;
  PN_stdfloat _rel_pos_x, _rel_pos_y;
  LVector2 _size;
  bool _visible;

  // Z-Index, relative to the parent
  float _local_z_index;

  // Z-Index, absolute
  float _z_index;

  // Wheter we already registered the element at the LUIRoot for recieving events
  bool _events_registered;

  bool _in_update_section;
  bool _snap_position;

  PT(LUIBounds) _margin;
  PT(LUIBounds) _padding;

  pmap<string, PT(CallbackObject)> _events;

  LUIBaseElement *_parent;
  LUIRoot *_root;

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
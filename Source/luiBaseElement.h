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

class LUIRoot;

NotifyCategoryDecl(luiBaseElement, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIBaseElement : public TypedReferenceCount {

  friend class LUIObject;

PUBLISHED:

  LUIBaseElement(PyObject *self);
  virtual ~LUIBaseElement();

  // Events
  INLINE void bind(const string &event_name, PyObject* callback);
  INLINE void bind(const string &event_name, CallbackObject* callback);
  INLINE void unbind(const string &event_name);
  INLINE bool has_event(const string &event_name);
  INLINE void trigger_event(const string &event_name, const string &message = string(), const LPoint2 &coords = LPoint2(0));

  // Position
  INLINE void set_top_left(float top, float left);
  INLINE void set_pos(float top, float left);
  INLINE void set_top(float top);
  INLINE void set_bottom(float bottom);
  INLINE void set_left(float left);
  INLINE void set_right(float right);
  INLINE LVector2 get_abs_pos();
  INLINE LVector2 get_pos();
  INLINE float get_top();
  INLINE float get_left();

  INLINE void set_centered();
  INLINE void set_centered_vertical();
  INLINE void set_centered_horizontal();

  // Margin
  INLINE void set_margin(float top, float right, float bottom, float left);
  INLINE void set_margin_top(float top);
  INLINE void set_margin_right(float right);
  INLINE void set_margin_bottom(float bottom);
  INLINE void set_margin_left(float left);

  INLINE float get_margin_top();
  INLINE float get_margin_right();
  INLINE float get_margin_bottom();
  INLINE float get_margin_left();

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
  INLINE float get_absolute_z_offset();

  INLINE LUIBaseElement* get_parent();

  INLINE virtual bool intersects(float x, float y);

  EXTENSION(int __setattr__(PyObject *self, PyObject* name, PyObject *value));
  EXTENSION(PyObject *__getattr__(PyObject *self, PyObject *name));


  INLINE void begin_update_section();
  INLINE virtual void end_update_section();


public:

  INLINE void set_parent(LUIBaseElement* parent);
  void recompute_position();

  INLINE void set_snap_position(bool snap);

  virtual void ls(int ident = 0) = 0;

protected:

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

  INLINE void recompute_z_index();
  void register_events();
  void unregister_events();

  PN_stdfloat _offset_x, _offset_y;
  LUIPlacementMode _placement_x, _placement_y;
  PN_stdfloat _pos_x, _pos_y;
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

  // Top, right, bottom, left
  float _margin[4];

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
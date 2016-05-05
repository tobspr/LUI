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
class LUIEventData;

NotifyCategoryDecl(luiBaseElement, EXPCL_LUI, EXPTP_LUI);

/**
 * @brief Base class for all LUI objects
 * @details This is the base class from which every LUI object derives. It stores
 *   information like the position, alignment and size, and also defines a common
 *   interface.
 */
class EXPCL_LUI LUIBaseElement : public TypedReferenceCount, public LUIColorable {

  friend class LUIObject;
  friend class LUIText;

PUBLISHED:
  LUIBaseElement(PyObject* self);
  virtual ~LUIBaseElement();

  // Events
  INLINE void bind(const string& event_name, CallbackObject* callback);
  INLINE void unbind(const string& event_name);
  INLINE void unbind_all();

  INLINE bool has_event(const string& event_name);
  void trigger_event(const string& event_name, const wstring& message = wstring(),
                     const LPoint2& coords = LPoint2(0));
  void trigger_event(PT(LUIEventData) data);

  // NAME
  INLINE void set_name(const string& name);
  INLINE const string& get_name() const;

  // Position
  INLINE void set_top_left(const LPoint2& pos);
  INLINE void set_top_right(const LPoint2& pos);
  INLINE void set_bottom_left(const LPoint2& pos);
  INLINE void set_bottom_right(const LPoint2& pos);

  INLINE LPoint2 get_top_left() const;
  INLINE LPoint2 get_top_right() const;
  INLINE LPoint2 get_bottom_left() const;
  INLINE LPoint2 get_bottom_right() const;

  INLINE void set_pos(const LPoint2& pos);
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

  INLINE void set_centered(bool center_vert = true, bool center_horiz = true);
  INLINE void set_center_vertical(bool centered = true);
  INLINE void set_center_horizontal(bool centered = true);

  INLINE bool is_centered() const;
  INLINE bool is_vertical_centered() const;
  INLINE bool is_horizontal_centered() const;

  // Margin
  INLINE void set_margin(const LVector4& margin);
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
  INLINE LUIBounds& get_margin();
  INLINE const LUIBounds& get_margin() const;

  // Padding
  INLINE void set_padding(const LVector4& padding);
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
  INLINE LUIBounds& get_padding();
  INLINE const LUIBounds& get_padding() const;

  // Size
  INLINE void set_size(const LVector2& size);
  INLINE void set_size(float width, float height);
  INLINE void set_size(const string& width, float height);
  INLINE void set_size(const string& width, const string& height);
  INLINE void set_size(float width, const string& height);
  INLINE void set_width(float width);
  INLINE void set_height(float height);
  INLINE void set_width(const string& width);
  INLINE void set_height(const string& height);
  INLINE float get_width() const;
  INLINE float get_height() const;
  INLINE void clear_width();
  INLINE void clear_height();
  INLINE void clear_size();
  INLINE bool has_width() const;
  INLINE bool has_height() const;
  INLINE bool has_size() const;
  INLINE LVector2 get_size() const;

  // Visible
  INLINE void set_visible(bool visible);
  INLINE bool is_visible() const;
  INLINE void hide();
  INLINE void show();

  // Solid
  INLINE void set_solid(bool solid);
  INLINE bool get_solid() const;

  // Z-Index
  void set_z_offset(float z_offset);
  INLINE float get_z_offset() const;

  // Focus
  INLINE bool has_focus() const;
  bool request_focus();
  void blur();

  INLINE bool has_parent() const;
  void clear_parent();
  void set_parent(LUIObject* parent);
  INLINE LUIObject* get_parent() const;

  INLINE virtual bool intersects(float x, float y) const;

  INLINE void clear_clip_bounds();
  INLINE void set_clip_bounds(const LUIBounds& bounds);
  INLINE void set_clip_bounds(float top, float right, float bottom, float left);
  INLINE const LUIBounds& get_clip_bounds() const;
  INLINE const LUIRect& get_abs_clip_bounds() const;

  INLINE bool is_topmost() const;
  INLINE void set_topmost(bool topmost);

  INLINE LVector2 get_relative_pos(const LPoint2& pos) const;
  INLINE void set_debug_name(const string& debug_name);
  INLINE const string& get_debug_name() const;

  // Properties for python
  MAKE_PROPERTY(name, get_name, set_name);
  MAKE_PROPERTY(debug_name, get_debug_name, set_debug_name);

  MAKE_PROPERTY(top_left, get_top_left, set_top_left);
  MAKE_PROPERTY(top_right, get_top_right, set_top_right);
  MAKE_PROPERTY(bottom_left, get_bottom_left, set_bottom_left);
  MAKE_PROPERTY(bottom_right, get_bottom_right, set_bottom_right);

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

  MAKE_PROPERTY2(size, has_size, get_size, set_size, clear_size);
  MAKE_PROPERTY2(width, has_width, get_width, set_width, clear_width);
  MAKE_PROPERTY2(height, has_height, get_height, set_height, clear_height);

  MAKE_PROPERTY(visible, is_visible, set_visible);
  MAKE_PROPERTY(z_offset, get_z_offset, set_z_offset);
  MAKE_PROPERTY(focused, has_focus);
  MAKE_PROPERTY2(parent, has_parent, get_parent, set_parent, clear_parent);

  MAKE_PROPERTY(clip_bounds, get_clip_bounds, set_clip_bounds);
  MAKE_PROPERTY(topmost, is_topmost, set_topmost);
  MAKE_PROPERTY(solid, get_solid, set_solid);

public:

  INLINE float get_x_extent() const;
  INLINE float get_y_extent() const;
  INLINE void do_set_parent(LUIObject* parent);
  INLINE void set_snap_position(bool snap);

  virtual void ls(int ident = 0) = 0;

  INLINE void set_focus(bool focus);
  INLINE int get_last_frame_visible() const;
  INLINE int get_last_render_index() const;

  INLINE void do_set_z_offset(int z_offset);

  virtual void update_dimensions_upstream();
  virtual void update_downstream();
  virtual void update_upstream();
  virtual void update_clip_bounds();

  void move_by(const LVector2& offset);

protected:

  virtual void update_dimensions();
  virtual void update_position();
  LVector2 get_available_dimensions() const;

  void load_python_events(PyObject* self);

  float get_parent_width() const;
  float get_parent_height() const;

  void fetch_render_index();

  enum LUIPlacementMode {
    // Stick to left/top
    M_default,

    // Stick to right/bottom
    M_inverse,

    // Center (either horizontally or vertically)
    M_center
  };

  // Interface
  virtual void set_root(LUIRoot* root) = 0;
  virtual void on_detached() = 0;

  virtual void render_recursive(bool is_topmost_pass, bool render_anyway) = 0;

  void register_events();
  void unregister_events();

  // Relative position
  LPoint2 _position;

  // Absolute position
  LPoint2 _abs_position;
  LVector2 _effective_size;

  // Placement modes
  struct {
    LUIPlacementMode x, y;
  } _placement;

  struct {
    LUIExpression x, y;
  } _size;

  bool _visible;

  // Z-Offset, relative to the parent
  float _z_offset;

  bool _events_registered;
  bool _snap_position;
  bool _focused;
  bool _solid;

  // Margin and padding, relative to the element bounds
  LUIBounds _margin;
  LUIBounds _padding;

  // Clip bounds, relative to the element bounds
  LUIBounds _clip_bounds;
  bool _have_clip_bounds;

  // Clip bounds, in absolute space
  LUIRect _abs_clip_bounds;

  pmap<string, PT(CallbackObject)> _events;

  LUIObject* _parent;
  LUIRoot* _root;

  int _last_frame_visible;
  int _last_render_index;
  bool _topmost;

  string _debug_name;
  string _name;

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

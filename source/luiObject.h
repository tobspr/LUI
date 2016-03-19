// Filename: luiNode.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_NODE_H
#define LUI_NODE_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "referenceCount.h"
#include "internalName.h"
#include "luse.h"
#include "luiAtlas.h"
#include "luiBaseElement.h"
#include "luiSprite.h"
#include "luiAtlasPool.h"
#include "luiAtlasDescriptor.h"
#include "luiIterators.h"
#include "luiColorable.h"

#include "config_lui.h"

class LUISprite;
class LUIRoot;

NotifyCategoryDecl(luiObject, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIObject : public LUIBaseElement {

  friend class LUIRoot;

PUBLISHED:

  LUIObject(PyObject* self, float x=0.0f, float y=0.0f,
           float w=-1.0f, float h=-1.0f, bool solid=false);
  LUIObject(PyObject* self, LUIObject* parent, float x=0.0, float y=0.0,
           float w=-1.0f, float h=-1.0f, bool solid=false);

  virtual ~LUIObject();

  INLINE PT(LUIElementIterator) get_children() const;
  INLINE PT(LUIBaseElement) get_child(size_t index) const;
  INLINE PT(LUIBaseElement) add_child(PT(LUIBaseElement) child);
  INLINE void remove_child(PT(LUIBaseElement) child);
  INLINE void remove_all_children();
  INLINE int get_child_count() const;

  INLINE void set_content_node(PT(LUIObject) content_node);
  INLINE PT(LUIObject) get_content_node() const;

  virtual void ls(int indent = 0);

  // Python properties
  MAKE_PROPERTY(children, get_children);
  MAKE_PROPERTY(child_count, get_child_count);
  MAKE_PROPERTY(content_node, get_content_node, set_content_node);

public:

  INLINE void on_child_z_offset_changed();
  void update_downstream();
  void update_upstream();
  void update_clip_bounds();
  void update_dimensions_upstream();

  void move_by(const LVector2& offset);

  void fit_dimensions();

protected:
  void update_dimensions();
  void init();

  // Interface to LUIBaseElement
  INLINE virtual void on_detached();
  virtual void set_root(LUIRoot* root);
  virtual void render_recursive(bool is_topmost_pass, bool render_anyway);

  pvector<PT(LUIBaseElement)> _children;
  PT(LUIObject) _content_node;

  static int _instance_count;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LUIBaseElement::init_type();
    register_type(_type_handle, "LUIObject", LUIBaseElement::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "luiObject.I"

#endif

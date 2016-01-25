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

typedef pvector<PT(LUIBaseElement)> LUIChildVector;

NotifyCategoryDecl(luiObject, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIObject : public LUIBaseElement {

  friend class LUIRoot;

PUBLISHED:

  LUIObject(PyObject *self, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0, bool solid = false);
  LUIObject(PyObject *self, LUIObject *parent, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0, bool solid = false);

  virtual ~LUIObject();

  INLINE PT(LUIElementIterator) get_children();
  INLINE PT(LUIBaseElement) add_child(PT(LUIBaseElement) child);
  INLINE void remove_child(PT(LUIBaseElement) child);
  INLINE void remove_all_children();

  INLINE void set_sort_children(bool do_sort);
  INLINE bool get_sort_children();

  INLINE int get_child_count();

  INLINE void fit_to_children();
  INLINE void fit_height_to_children();
  INLINE void fit_width_to_children();

  INLINE void set_content_node(PT(LUIObject) content_node);
  INLINE PT(LUIObject) get_content_node();

  virtual void ls(int indent = 0);

  // Python properties
  MAKE_PROPERTY(children, get_children);
  MAKE_PROPERTY(child_count, get_child_count);
  MAKE_PROPERTY(sort_children, get_sort_children, set_sort_children);

protected:

  void init();

  // Interface to LUIBaseElement
  INLINE virtual void on_bounds_changed();
  INLINE virtual void on_visibility_changed();
  INLINE virtual void on_detached();
  virtual void set_root(LUIRoot* root);
  virtual void render_recursive(bool is_topmost_pass, bool render_anyway);

  // Interface to LUIColorable
  INLINE virtual void on_color_changed();

  LUIChildVector _children;
  PT(LUIObject) _content_node;
  bool _sort_children;



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

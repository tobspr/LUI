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

#include "config_lui.h"

class LUISprite;
class LUIRoot;

NotifyCategoryDecl(luiObject, EXPCL_LUI, EXPTP_LUI);

class EXPCL_LUI LUIObject : public LUIBaseElement {

  friend class LUIRoot;

PUBLISHED:
  
  LUIObject(float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0);
  LUIObject(LUIObject *parent, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0);

  virtual ~LUIObject();

  INLINE LUISprite *attach_sprite(const string &source, float x, float y, float w = 0.0, float h = 0.0);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id, float x, float y, float w = 0.0, float h = 0.0);
  INLINE LUISprite *attach_sprite(PT(Texture) tex, float x, float y, float w = 0.0, float h = 0.0);

  INLINE LUISprite *attach_sprite(const string &source);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id);
  INLINE LUISprite *attach_sprite(PT(Texture) tex);

  PT(LUIElementIterator) children();

  INLINE PT(LUIBaseElement) add_child(PT(LUIBaseElement) child);
  INLINE void remove_child(PT(LUIBaseElement) child);
  INLINE void remove_all_children();

  INLINE int get_child_count();

  virtual void ls(int indent = 0);



protected:

  void init();

  // Interface to LUIBaseElement
  void on_bounds_changed();
  void on_visibility_changed();
  void on_detached();
  void set_root(LUIRoot* root);
  void on_z_index_changed();
  

  PT(LUISprite) construct_and_attach_sprite(float x, float y, float w, float h);
  INLINE void refresh_child_positions();
  INLINE void refresh_child_visibility();

  pset<PT(LUIBaseElement)> _children;

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
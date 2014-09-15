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

class EXPCL_PANDASKEL LUIObject : public ReferenceCount, public LUIBaseElement {

  friend class LUIRoot;

PUBLISHED:
  
  LUIObject(float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0);
  LUIObject(LUIObject *parent, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0);

  ~LUIObject();

  INLINE LUISprite *attach_sprite(const string &source, float x, float y, float w = 0.0, float h = 0.0);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id, float x, float y, float w = 0.0, float h = 0.0);
  INLINE LUISprite *attach_sprite(PT(Texture) tex, float x, float y, float w = 0.0, float h = 0.0);

  INLINE LUISprite *attach_sprite(const string &source);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id);
  INLINE LUISprite *attach_sprite(PT(Texture) tex);

  INLINE void remove_sprite(PT(LUISprite) sprite);
  INLINE int get_sprite_count();

  PT(LUISpriteIterator) sprites();

  INLINE PT(LUIObject) add_child(PT(LUIObject) node);
  INLINE void remove_child(PT(LUIObject) node);

  void ls(int indent = 0);

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


  pset<PT(LUIObject)> _nodes;
  pset<PT(LUISprite)> _sprites;

  static int _instance_count;

};

#include "luiObject.I"

#endif
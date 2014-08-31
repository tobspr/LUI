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

#include "config_lui.h"

class LUISprite;
class LUIRoot;


class EXPCL_PANDASKEL LUINode : public ReferenceCount, public LUIBaseElement {

  friend class LUIRoot;

PUBLISHED:

  LUINode(float w, float h);
  ~LUINode();

  INLINE LUISprite *attach_sprite(const string &source, float x, float y);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id, float x, float y);
  INLINE LUISprite *attach_sprite(PT(Texture) tex, float x, float y);

  INLINE LUISprite *attach_sprite(const string &source);
  INLINE LUISprite *attach_sprite(const string &source, const string &atlas_id);
  INLINE LUISprite *attach_sprite(PT(Texture) tex);

  INLINE void remove_sprite(PT(LUISprite) sprite);
  INLINE int get_sprite_count();
  INLINE PT(LUISprite) get_sprite(int n);
  INLINE PT(LUINode) add_child(PT(LUINode) node);
  INLINE void remove_child(PT(LUINode) node);
  // TODO: Add remove_child

protected:


  // Interface to LUIBaseElement
  void on_bounds_changed();
  void on_visibility_changed();
  void on_detached();
  void set_root(LUIRoot* root);
  

  PT(LUISprite) construct_and_attach_sprite(float x, float y);
  INLINE void refresh_child_positions();
  INLINE void refresh_child_visibility();


  pvector<PT(LUINode)> _nodes;
  pvector<PT(LUISprite)> _sprites;

  static int _instance_count;

};

#include "luiNode.I"

#endif
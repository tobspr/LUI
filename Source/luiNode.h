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
#include "luiSprite.h"
#include "luiNode.h"
#include "luiAtlasPool.h"
#include "luiAtlasDescriptor.h"
#include "luiBaseElement.h"
#include "config_lui.h"

class LUISprite;
class LUIRoot;

class EXPCL_PANDASKEL LUINode : public ReferenceCount, public LUIBaseElement {

PUBLISHED:

  LUINode(float w, float h);
  ~LUINode();

  INLINE PT(LUIAtlasDescriptor) get_atlas_image(const string &identifier);
  INLINE PT(LUIAtlasDescriptor) get_atlas_image(const string &atlas_id, const string &identifier);

  INLINE PT(LUISprite) attach_sprite(const string &source, float x, float y);
  INLINE PT(LUISprite) attach_sprite(const string &source, const string &atlas_id, float x, float y);
  INLINE PT(LUISprite) attach_sprite(PT(Texture) tex, float x, float y);

  INLINE PT(LUISprite) attach_sprite(const string &source);
  INLINE PT(LUISprite) attach_sprite(const string &source, const string &atlas_id);
  INLINE PT(LUISprite) attach_sprite(PT(Texture) tex);

  INLINE void remove_sprite(PT(LUISprite) sprite);
  INLINE int get_sprite_count();
  INLINE PT(LUISprite) get_sprite(int n);

  void operator += (PT(LUINode) node);
private:

  // Interface to LUIBaseElement
  void on_bounds_changed();
  void on_visibility_changed();

  PT(LUISprite) construct_and_attach_sprite(float x, float y);
  INLINE void refresh_sprite_positions();
  INLINE void refresh_sprite_visibility();

  vector<PT(LUINode)> _nodes;
  vector<PT(LUISprite)> _sprites;

  LUIRoot* _root;

};

#include "luiNode.I"

#endif
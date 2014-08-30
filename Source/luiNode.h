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
#include "config_lui.h"

class LUISprite;
class LUIRoot;

class EXPCL_PANDASKEL LUINode : public ReferenceCount {

  PUBLISHED:

    LUINode(float w, float h);
    ~LUINode();
    
    INLINE PT(LUIAtlasDescriptor) get_atlas_image(const string &identifier);
    INLINE PT(LUIAtlasDescriptor) get_atlas_image(const string &atlas_id, const string &identifier);

    INLINE PT(LUISprite) attach_sprite(float x, float y, const string &source);
    INLINE PT(LUISprite) attach_sprite(float x, float y, PT(LUIAtlasDescriptor) desc);
    INLINE PT(LUISprite) attach_sprite(float x, float y, PT(Texture) tex);

    INLINE void remove_sprite(PT(LUISprite) sprite);

    INLINE int get_sprite_count();
    INLINE PT(LUISprite) get_sprite(int n);

    INLINE const LVector2 &get_size() const;
    INLINE void set_size(const LVector2 &size);
    INLINE void set_size(float w, float h);

    void operator += (PT(LUINode) node);


	private:

    PT(LUISprite) construct_and_attach_sprite(float x, float y);
    INLINE void refresh_sprite_positions();

    vector<LUINode> _nodes;
    vector<LUISprite*> _sprites;

    LVector2 _size;

    LUIRoot* _root;
    LUINode* _parent;

};

#include "luiNode.I"

#endif
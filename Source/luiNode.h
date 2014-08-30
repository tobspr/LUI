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
#include "config_lui.h"

class LUISprite;
class LUIRoot;

class EXPCL_PANDASKEL LUINode : public ReferenceCount {

  PUBLISHED:

    LUINode();
    ~LUINode();
  
    
    LUIAtlasDescriptor get_atlas_image(string identifier);

    PT(LUISprite) attach_sprite(float x, float y, LUIAtlasDescriptor desc);
    void operator += (PT(LUINode) node);

 
	private:

    vector<LUINode> _nodes;
    vector<LUISprite*> _sprites;

    LUIRoot* _root;

};

#endif
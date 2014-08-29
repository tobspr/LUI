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

class LUISprite;

class EXPCL_PANDASKEL LUINode : public ReferenceCount {

  PUBLISHED:

    LUINode();
    ~LUINode();
  
    void add_widget(LUINode *node);
    PT(LUISprite) attach_sprite(string identifier);

	private:

    vector<LUINode> _nodes;
    vector<LUISprite> _sprites;

};

#endif
// Filename: luiSprite.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_SPRITE_H
#define LUI_SPRITE_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"

#include "luiSprite.h"

class LUIVertexPool {

public:

    LUIVertexPool();
    ~LUIVertexPool();
		
	private:

     vector<LUISprite*> _sprite_slots;
     // todo


};

#endif
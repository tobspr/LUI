// Filename: luiVertexPool.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_VERTEX_POOL_H
#define LUI_VERTEX_POOL_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"
#include "luiSprite.h"

class LUIVertexPool {

public:

  LUIVertexPool(Texture *tex);
  ~LUIVertexPool();

private:

  PT(Texture) _tex;
  
};

#endif
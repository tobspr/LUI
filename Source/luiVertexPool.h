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
#include "luiVertexData.h"
#include "luiVertexChunk.h"
#include "luiChunkDescriptor.h"

#include "geomVertexFormat.h"
#include "geomVertexData.h"
#include "geomVertexWriter.h"
#include "geomTriangles.h"
#include "bitArray.h"
#include "geom.h"

class LUISprite;
class LUIVertexChunk;

class LUIVertexPool {

public:

  LUIVertexPool(Texture *tex);
  ~LUIVertexPool();

  LUIChunkDescriptor *allocate_slot(LUISprite *child);

private:

  void allocate_chunk();
  PT(Texture) _tex;
  vector<LUIVertexChunk*> _chunks;

};

#include "luiVertexPool.I"

#endif
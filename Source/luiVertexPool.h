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
#include "geomVertexFormat.h"
#include "geomVertexData.h"
#include "geomVertexWriter.h"
#include "bitArray.h"
#include "geom.h"

class LUIVertexPool {

public:

  LUIVertexPool(Texture *tex);
  ~LUIVertexPool();

  INLINE int allocate_slot();
  INLINE void release_slot(int slot);
  INLINE void* get_sprite_pointer(int slot);

private:

  PT(Texture) _tex;
  PT(GeomVertexData) _vertex_data;
  BitArray _slots;
  
  int _sprite_count;
  int _highest_index;

};

#include "luiVertexPool.I"

#endif
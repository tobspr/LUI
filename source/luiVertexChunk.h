// Filename: luiVertexChunk.h
// Created by:  tobspr (02Sep14)
//

#ifndef LUI_VERTEX_CHUNK_H
#define LUI_VERTEX_CHUNK_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"
#include "luiSprite.h"
#include "luiVertexData.h"
#include "luiSprite.h"
#include "geomVertexFormat.h"
#include "geomVertexData.h"
#include "geomVertexWriter.h"
#include "geomTriangles.h"
#include "geom.h"

class LUISprite;

class LUIVertexChunk {

public:

  LUIVertexChunk(int chunk_size);
  ~LUIVertexChunk();

  INLINE bool is_empty() const;
  INLINE bool has_space() const;
  INLINE Geom* get_geom() const;

  INLINE int reserve_slot(LUISprite* sprite);
  INLINE void free_slot(int slot);
  INLINE void* get_slot_ptr(int slot) const;

private:

  PT(GeomVertexData) _vertex_data;
  PT(GeomTriangles) _triangles;
  PT(Geom) _geom;

  int _sprite_count;
  int _chunk_size;
  void* _write_pointer;
  LUISprite** _children;

};

#include "luiVertexChunk.I"

#endif

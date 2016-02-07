// Filename: luiVertexPool.h
// Created by:  tobspr (28Aug14)
//


#ifndef LUI_CHUNK_DESCRIPTOR_H
#define LUI_CHUNK_DESCRIPTOR_H

#include "pandabase.h"
#include "pandasymbols.h"

class LUIVertexChunk;

class LUIChunkDescriptor {

  // Give only LUIVertexPool the permission to set the initial values
  friend class LUIVertexPool;

private:

  LUIChunkDescriptor();

  INLINE void set_slot(int slot);
  INLINE void set_chunk(LUIVertexChunk* chunk);

  LUIVertexChunk* _chunk;
  int _slot;

public:

  ~LUIChunkDescriptor();

  void release();
  void* get_write_ptr() const;
  INLINE int get_slot() const;
  INLINE LUIVertexChunk* get_chunk() const;
};


#include "luiChunkDescriptor.I"




#endif

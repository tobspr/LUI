// Filename: luiSprite.h
// Created by:  tobspr (26Aug14)
//

#ifndef LUI_SPRITE_H
#define LUI_SPRITE_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"
#include "referenceCount.h"
#include "config_lui.h"
#include "luiBaseElement.h"
#include "luiAtlasDescriptor.h"
#include "luiAtlasPool.h"
#include "luiVertexPool.h"
#include "texturePool.h"

#include <iostream>

class LUIVertexPool;
class LUINode;


////////////////////////////////////////////////////////////////////
//       Class : LUISprite
// Description : A LUISprite stores a single card, including position,
//               scale, and uv coordinates. It also notifies the
//               LUIVertexPool when any scalar or texture got changed.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDASKEL LUISprite : public ReferenceCount, public LUIBaseElement  {

  friend class LUINode;

PUBLISHED:

  // Texcoord
  INLINE void set_uv_range(const LTexCoord &uv_begin, const LTexCoord &uv_end);
  INLINE void get_uv_range(LTexCoord &uv_begin, LTexCoord &uv_end);

  // Color
  INLINE void set_color(const LColor &color);
  INLINE void set_color(float r, float g, float b, float a);
  INLINE LColor get_color();

  // Texture
  INLINE void set_texture(Texture* tex);
  INLINE void set_texture(LUIAtlasDescriptor *descriptor);
  INLINE void set_texture(const string &source);
  INLINE Texture *get_texture() const;

  // Z-Index
  INLINE void set_z_index(float z_index);
  INLINE float get_z_index();

  INLINE void print_vertices();

public:

  LUISprite(LUIBaseElement* parent);
  ~LUISprite();

  INLINE void set_pool_slot(int slot);
  INLINE int get_pool_slot();

  struct LUIVertexData {
    PN_stdfloat x, y, z;
    PN_stdfloat u, v;
    PN_stdfloat color[4];
  };

protected:

  INLINE void recompute_vertices();
  void assign_vertex_pool();
  void unassign_vertex_pool();

  // Interface to LUIBaseElement
  void on_bounds_changed();
  void on_visibility_changed();
  void on_detached();
  void set_root(LUIRoot* root);

  // Stores data for 4 corner vertices
  // 0 - Upper Left
  // 1 - Upper Right
  // 2 - Lower Right
  // 3 - Lower Left
  LUIVertexData _data[4];

  // Index in the LUIVertexPool
  int _pool_slot;

  // Handle to the LUIVertexPool
  LUIVertexPool* _vertex_pool;

  PT(Texture) _tex;

  // Keep track of the amount of instances created, for 
  // tracking memory leaks
  static int _instance_count;

};


#include "luiSprite.I"

#endif
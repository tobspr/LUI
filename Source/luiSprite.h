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
#include "luiVertexData.h"
#include "luiVertexChunk.h"
#include "luiChunkDescriptor.h"
#include "luiColorable.h"
#include "texturePool.h"
#include <iostream>


class LUIVertexPool;
class LUIObject;
class LUIChunkDescriptor;


NotifyCategoryDecl(luiSprite, EXPCL_LUI, EXPTP_LUI);

////////////////////////////////////////////////////////////////////
//       Class : LUISprite
// Description : A LUISprite stores a single card, including position,
//               scale, and uv coordinates. It also notifies the
//               LUIVertexPool when any scalar or texture got changed.
////////////////////////////////////////////////////////////////////
class EXPCL_LUI LUISprite : public LUIBaseElement  {

  friend class LUIObject;

PUBLISHED:

  
  // Initialize with a path to an image  
  LUISprite(PyObject *self, LUIObject* parent, const string &image, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0, const LColor &color = LColor(1));
  
  // Initialize with a texture handle
  LUISprite(PyObject *self, LUIObject* parent, Texture *texture, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0, const LColor &color = LColor(1));
  
  // Initialize with a atlas entry
  LUISprite(PyObject *self, LUIObject* parent, const string &entry_id, const string &atlas_id, float x = 0.0, float y = 0.0, float w = 0.0, float h = 0.0, const LColor &color = LColor(1));

  virtual ~LUISprite();

  // Texcoord
  INLINE void set_uv_range(const LTexCoord &uv_begin, const LTexCoord &uv_end);
  INLINE void set_uv_range(float u0, float v0, float u1, float v1);
  INLINE void get_uv_range(LTexCoord &uv_begin, LTexCoord &uv_end);

  // Texture
  INLINE void set_texture(Texture* tex, bool resize=true);
  INLINE void set_texture(LUIAtlasDescriptor *descriptor, bool resize=true);
  INLINE void set_texture(const string &source, bool resize=true);
  INLINE void set_texture(const string &entry_name, const string &atlas_id, bool resize=true);
  INLINE Texture *get_texture() const;

  INLINE void print_vertices();

  void ls(int indent = 0);

  // Python properties
  MAKE_PROPERTY(texture, get_texture);
  
protected:

  void init(LUIObject *parent, float x, float y, const LColor &color);
  INLINE void init_size(float w, float h);

  INLINE void recompute_vertices();
  void update_vertex_pool();
  void assign_vertex_pool();
  void unassign_vertex_pool();

  // Interface to LUIBaseElement
  INLINE void on_bounds_changed();
  INLINE void on_visibility_changed();
  INLINE void on_detached();
  void set_root(LUIRoot* root);
  INLINE void on_z_index_changed();

  // Interface to LUIColorable
  void on_color_changed();

  // Stores data for 4 corner vertices
  // 0 - Upper Left
  // 1 - Upper Right
  // 2 - Lower Right
  // 3 - Lower Left
  LUIVertexData _data[4];

  // Handle to the LUIVertexPool
  LUIChunkDescriptor *_chunk_descriptor;

  PT(Texture) _tex;

  // Keep track of the amount of instances created, for 
  // tracking memory leaks
  static int _instance_count;


public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    LUIBaseElement::init_type();
    register_type(_type_handle, "LUISprite", LUIBaseElement::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;


};


#include "luiSprite.I"

#endif
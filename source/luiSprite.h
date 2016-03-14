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

class LUIVertexPool;
class LUIObject;
class LUIChunkDescriptor;
class LUIText;

NotifyCategoryDecl(luiSprite, EXPCL_LUI, EXPTP_LUI);

////////////////////////////////////////////////////////////////////
//       Class : LUISprite
// Description : A LUISprite stores a single card, including position,
//               scale, and uv coordinates. It also notifies the
//               LUIVertexPool when any scalar or texture got changed.
////////////////////////////////////////////////////////////////////
class EXPCL_LUI LUISprite : public LUIBaseElement  {

  friend class LUIObject;
  friend class LUIText;

  // Initialize empty with just a parent this is for the LUIText
  explicit LUISprite(LUIText* parent_text);

PUBLISHED:

  // Initialize with a path to an image
  LUISprite(PyObject* self, LUIObject* parent, const string& image,
            float x=0.0f, float y=0.0f, float w=0.0f, float h=0.0f, const LColor& color=LColor(1));

  // Initialize with a texture handle
  LUISprite(PyObject* self, LUIObject* parent, Texture* texture,
            float x=0.0f, float y=0.0f, float w=0.0f, float h=0.0f, const LColor& color=LColor(1));

  // Initialize with a atlas entry
  LUISprite(PyObject* self, LUIObject* parent, const string& entry_id, const string& atlas_id,
            float x=0.0f, float y=0.0f, float w=0.0f, float h=0.0f, const LColor& color=LColor(1));

  virtual ~LUISprite();

  // Texcoord
  INLINE void set_uv_range(const LTexCoord& uv_begin, const LTexCoord& uv_end);
  INLINE void set_uv_range(float u0, float v0, float u1, float v1);
  INLINE const LTexCoord& get_uv_begin() const;
  INLINE const LTexCoord& get_uv_end() const;

  // Texture
  INLINE void set_texture(Texture* tex, bool resize=true);
  INLINE void set_texture(const LUIAtlasDescriptor& descriptor, bool resize=true);
  INLINE void set_texture(const string& source, bool resize=true);
  INLINE void set_texture(const string& entry_name, const string& atlas_id, bool resize=true);
  INLINE Texture* get_texture() const;

  INLINE void print_vertices();

  void ls(int indent = 0);

  // Python properties
  MAKE_PROPERTY(texture, get_texture);

protected:

  void init(LUIObject* parent, float x, float y, const LColor& color);
  INLINE void init_size(float w, float h);

  void recompute_vertices();
  void update_vertex_pool();
  void assign_sprite_index();
  void unassign_sprite_index();

  // Interface to LUIBaseElement
  INLINE void on_detached();
  void set_root(LUIRoot* root);

  virtual void render_recursive(bool is_topmost_pass, bool render_anyway);

  void fetch_texture_index();

  // Stores data for 4 corner vertices
  // 0 - Upper Left
  // 1 - Upper Right
  // 2 - Lower Right
  // 3 - Lower Left
#ifndef CPPPARSER  // Interrogate sucks at parsing the next line
  LUIVertexData _data[4];
#endif

  // Stores texture coordinates
  LTexCoord _uv_begin;
  LTexCoord _uv_end;

  PT(Texture) _tex;

  // Keep track of the amount of instances created, for
  // tracking memory leaks
  static int _instance_count;

  int _texture_index;
  int _sprite_index;

  string _debug_source;

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

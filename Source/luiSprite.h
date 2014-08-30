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
#include "luiAtlasDescriptor.h"
#include "luiAtlasPool.h"
#include "texturePool.h"
#include "luiBaseElement.h"

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

PUBLISHED:

    // Texcoord
		INLINE void set_texcoord_start(const LVector2 &texcoord_start);
    INLINE void set_texcoord_start(float u, float v);
		INLINE LVector2 get_texcoord_start();
		
		INLINE void set_texcoord_end(const LVector2 &texcoord_end);
    INLINE void set_texcoord_end(float u, float v);
		INLINE LVector2 get_texcoord_end();
		
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
	
  public:

    LUISprite(LUINode* parent);
    ~LUISprite();

    INLINE void set_pool_slot(int slot);
    INLINE int get_pool_slot();

	protected:

    INLINE void recompute_vertices();

    // Interface to LUIBaseElement
    LVector2 get_parent_size();
    void on_position_changed();
    void on_size_changed();
    void on_visibility_changed();
    
		struct LUIVertexData {
        PN_stdfloat x, y, z;
        PN_stdfloat u, v;
        PN_stdfloat color[4];
    };
    
    // Stores data for 4 corner vertices
    // 0 - Upper Left
    // 1 - Upper Right
    // 2 - Lower Right
    // 3 - Lower Left
    LUIVertexData _data[4];

    // Index in the LUIVertexPool
    int         _pool_slot;

    // Handle to the LUIVertexPool
    LUIVertexPool* _vertex_pool;

    PT(Texture) _tex;

};


#include "luiSprite.I"

#endif
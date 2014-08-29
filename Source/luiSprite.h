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
#include <iostream>

class LUIVertexPool;

////////////////////////////////////////////////////////////////////
//       Class : LUISprite
// Description : A LUISprite stores a single card, including position,
//               scale, and uv coordinates. It also notifies the
//               LUIVertexPool when any scalar or texture got changed.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDASKEL LUISprite : public ReferenceCount {

PUBLISHED:

    LUISprite();
    ~LUISprite();

		// Setter / Getter 
		INLINE void set_pos(const LPoint2 &pos);
    INLINE void set_pos(float x, float y);
		INLINE LPoint2 get_pos();

		INLINE void set_size(const LVector2 &size);
    INLINE void set_size(float x, float y);
		INLINE const LVector2 &get_size() const;

		INLINE void set_texcoord_start(const LVector2 &texcoord_start);
    INLINE void set_texcoord_start(float u, float v);
		INLINE LVector2 get_texcoord_start();
		
		INLINE void set_texcoord_end(const LVector2 &texcoord_end);
    INLINE void set_texcoord_end(float u, float v);
		INLINE LVector2 get_texcoord_end();
		
    INLINE void set_color(const LColor &color);
    INLINE void set_color(float r, float g, float b, float a);
    INLINE LColor get_color();

		INLINE void set_texture(Texture* tex);
		INLINE Texture* get_texture() const;

		INLINE void set_z_index(float z_index);
		INLINE float get_z_index();
		
		INLINE void set_visible(bool visible);
		INLINE bool is_visible();

		// Shortcuts for set_visible
		INLINE void hide();
		INLINE void show();
		
  public:

    INLINE void set_pool_slot(int slot);
    INLINE int get_pool_slot();

	protected:

    INLINE void update_vertices();
    INLINE bool is_valid_coord(float x, float y);

		struct LUIVertexData {
        float x;
        float y;
        float z;
        float u;
        float v;
        float color[4];
    };

    // Stores data for 4 corner vertices
    // 0 - Upper Left
    // 1 - Upper Right
    // 2 - Lower Right
    // 3 - Lower Left
    LUIVertexData _data[4];

		// XY Size of the sprite, there is no scale
		LVector2    _size;
		
		// Determines wheter the sprite will get rendered
		bool	      _visible;

    // Index in the LUIVertexPool
    int         _pool_slot;

    // Handle to the LUIVertexPool
    LUIVertexPool* _vertex_pool;

};

#include "luiSprite.I"

#endif
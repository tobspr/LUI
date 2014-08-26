// Filename: LUISprite.h
// Created by:  tobspr (26Aug14)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#include "pandabase.h"
#include "lpoint2.h"
#include "lvector2.h"
#include "texture.h"
#include "referenceCount.h"


class LUISprite : public ReferenceCount {

		// Setter / Getter 
		INLINE void set_pos(LPoint2 &pos);
		INLINE LPoint2 &get_pos();

		INLINE void set_size(LVector2 &size);
		INLINE LVector2 &get_size();

		INLINE void set_texcoord_start(LVector2 &texcoord_start);
		INLINE LVector2 &get_texcoord_start();
		
		INLINE void set_texcoord_end(LVector2 &texcoord_end);
		INLINE LVector2 &get_texcoord_end();
		
		INLINE void set_color(LVecBase4f &color);
		INLINE LVecBase4f &get_color();

		INLINE void set_texture(PT(Texture) tex);
		INLINE PT(Texture) get_texture();

		INLINE void set_z_index(float z_index);
		INLINE float get_z_index();
		
		INLINE void set_visible(bool visible);
		INLINE bool is_visible();

		// Shortcuts for set_visible
		INLINE void hide();
		INLINE void show();
		
	private:
		// XY Position of the sprite
		LPoint2     _pos;

		// XY Size of the sprite, there is no scale
		LVector2    _size;

		// Card UV's
		LVector2    _texcoord_start;
		LVector2    _texcoord_end;
		
		// Color scale, including alpha
		LVecBase4   _color;

		// The actual sprite texture
		PT(Texture) _tex;

		// The z-index
		float	    _z_index;

		// Determines wheter the sprite will get rendered
		bool	    _visible;
};

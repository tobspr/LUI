// Filename: luiAtlasDescriptor.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_ATLAS_DESCRIPTOR_H
#define LUI_ATLAS_DESCRIPTOR_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"
#include "config_lui.h"

class LUIAtlasPool;

/**
 * @brief Class to store positions in a given atlas
 * @details This is a container class to store a reference to a sprite in an
 *   atlas. It stores a handle to the atlas texture, the size of the sprite
 *   in the atlas, and the uv start and end coordinates. This is the required
 *   information to render a sprite from that atlas.
 *
 *   The class is internally used by LUISprite to store the atlas position,
 *   whenever a texture from the atlas is used.
 */
class EXPCL_LUI LUIAtlasDescriptor {

  // Only the LUIAtlasPool is allowed to create new descriptors
  friend class LUIAtlasPool;
  LUIAtlasDescriptor();

  INLINE void set_texture(Texture* tex);
  INLINE void set_size(const LVector2& size);
  INLINE void set_uv_range(const LTexCoord& uv_begin, const LTexCoord& uv_end);

public:

  INLINE Texture* get_texture() const;
  INLINE const LVector2& get_size() const;
  INLINE const LTexCoord& get_uv_begin() const;
  INLINE const LTexCoord& get_uv_end() const;

private:

  Texture* _tex;
  LVector2 _size;
  LTexCoord _uv_begin;
  LTexCoord _uv_end;

};

#include "luiAtlasDescriptor.I"

#endif

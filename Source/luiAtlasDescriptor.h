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

class EXPCL_LUI LUIAtlasDescriptor : public ReferenceCount {

PUBLISHED:
  LUIAtlasDescriptor();
  ~LUIAtlasDescriptor();

public:

  INLINE Texture* get_texture() const;
  INLINE const LVector2 &get_size() const;
  INLINE const LTexCoord &get_uv_begin() const;
  INLINE const LTexCoord &get_uv_end() const;

  INLINE void set_texture(Texture* tex);
  INLINE void set_size(const LVector2 &size);
  INLINE void set_uv_range(const LTexCoord &uv_begin, const LTexCoord &uv_end);

private:

  // Todo: Add getters & setters
  Texture* _tex;
  LVector2 _size;
  LTexCoord _uv_begin;
  LTexCoord _uv_end;

  static int _instance_count;

};

#include "luiAtlasDescriptor.I"

#endif

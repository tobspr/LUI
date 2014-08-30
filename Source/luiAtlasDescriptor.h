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

class EXPCL_PANDASKEL LUIAtlasDescriptor : public ReferenceCount {

PUBLISHED:
  LUIAtlasDescriptor();
  ~LUIAtlasDescriptor();

public:

  INLINE Texture* get_texture() const;
  INLINE const LVector2 &get_size() const;
  INLINE const LVector2 &get_uv_begin() const;
  INLINE const LVector2 &get_uv_end() const;

  INLINE void set_texture(Texture* tex);
  INLINE void set_size(const LVector2 &size);
  INLINE void set_uv_begin(const LVector2 &uv_begin);
  INLINE void set_uv_end(const LVector2 &uv_end);

private:

  // Todo: Add getters & setters
  Texture* _tex;
  LVector2 _size;
  LVector2 _uv_begin;
  LVector2 _uv_end;


  static int _instance_count;

};

#include "luiAtlasDescriptor.I"

#endif
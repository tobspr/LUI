// Filename: luiAtlas.h
// Created by:  tobspr (29Aug14)
//

#ifndef LUI_ATLAS_H
#define LUI_ATLAS_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"

struct LUIAtlasDescriptor {
  Texture* tex;
  PN_stdfloat width, height;
  LVector2 uv_begin;
  LVector2 uv_end;
};

#endif
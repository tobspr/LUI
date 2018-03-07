// Filename: luiVertexData.h
// Created by:  tobspr (01Sep14)
//

#ifndef LUI_VERTEX_DATA_H
#define LUI_VERTEX_DATA_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"

#include <stdint.h>

struct LUIVertexData {
  float x, y, z;
  unsigned char color[4];
  float u, v;
  uint16_t texindex;
};

#endif

// Filename: luiAtlasPacker.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_ATLAS_PACKER_H
#define LUI_ATLAS_PACKER_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "lvector2.h"
#include "config_lui.h"
#include "referenceCount.h"

class EXPCL_LUI LUIAtlasPacker : public ReferenceCount {

PUBLISHED:

  LUIAtlasPacker(int size);
  ~LUIAtlasPacker();

  LVector2f find_position(int w, int h);

private:

  bool **values_bitmask;
  int _size;

};

#endif
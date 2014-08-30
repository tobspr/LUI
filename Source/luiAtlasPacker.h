// Filename: luiAtlasPacker.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_ATLAS_PACKER_H
#define LUI_ATLAS_PACKER_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "referenceCount.h"
#include "internalName.h"
#include "luse.h"
#include "config_lui.h"

class EXPCL_PANDASKEL LUIAtlasPacker : public ReferenceCount {

  PUBLISHED:
  
    LUIAtlasPacker(int size);
    ~LUIAtlasPacker();

    LVector2 find_position(int w, int h);

	private:
  
     bool **values_bitmask;
     int _size;

};

#endif
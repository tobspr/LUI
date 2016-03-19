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

/**
 * @brief Helper class used by the LUIAtlasPacker
 * @details This is a helper class which is used by the LUIAtlasPacker to generate
 *   an atlas. It provides functionality to find positions for sprites in a texture.
 *
 */
class EXPCL_LUI LUIAtlasPacker : public ReferenceCount {

PUBLISHED:

  LUIAtlasPacker(size_t size);
  ~LUIAtlasPacker();

  LVector2f find_position(size_t w, size_t h);

private:

  // Helper methods to access the interleaved array
  INLINE bool get_value(size_t x, size_t y) const      { return values_bitmask[x + y * _size]; }
  INLINE void set_value(size_t x, size_t y, bool flag) { values_bitmask[x + y * _size] = flag; }

  bool* values_bitmask;
  size_t _size;

};

#endif

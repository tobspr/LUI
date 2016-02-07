// Filename: luiAtlasPool.h
// Created by:  tobspr (30Aug14)
//

#ifndef LUI_ATLAS_POOL_H
#define LUI_ATLAS_POOL_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "filename.h"

#include "luiAtlas.h"
#include "luiAtlasDescriptor.h"

#include "config_lui.h"

/**
 * @brief Globals storage for multiple atlases
 * @details This class stores all atlases, and keeps a reference to them. It also
 *   provides methods to get a descriptor from a given entry name and atlas name.
 */
class EXPCL_LUI LUIAtlasPool {

PUBLISHED:

  static LUIAtlasPool* get_global_ptr();

  void load_atlas(const string& atlas_id, const string& atlas_desc_path, const string& atlas_tex_path);

  INLINE bool has_atlas(const string& atlas_id) const;
  INLINE PT(LUIAtlas) get_atlas(const string& atlas_id) const;
  INLINE LUIAtlasDescriptor get_descriptor(const string& atlas_id, const string& entry_id) const;

private:

  LUIAtlasPool();
  pmap<string, PT(LUIAtlas)> _atlases;
  static LUIAtlasPool* _global_ptr;
};

#include "luiAtlasPool.I"

#endif

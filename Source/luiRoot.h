// Filename: luiRoot.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_ROOT_H
#define LUI_ROOT_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "luiVertexPool.h"
#include "luiAtlas.h"
#include "luiObject.h"

#include "config_lui.h"

class LUIObject;

typedef pmap<Texture*, LUIVertexPool*> LUIVertexPoolMap;

class EXPCL_PANDASKEL LUIRoot : public ReferenceCount {

  friend class LUIRegion;

PUBLISHED:

  LUIRoot(float width, float height);
  ~LUIRoot();

  INLINE PT(LUIObject) node();

public:

  INLINE LUIVertexPool* get_vpool_by_texture(Texture* tex);

private:

  // Vertex pools are stored as single pointers, to avoid circular
  // references. The destructor of LUIRoot takes care of deleting them.
  LUIVertexPoolMap _pools;

  // We expose this to LUIRegion only, so it can iterate over all pools
  // in a fast way.
  INLINE LUIVertexPoolMap::iterator get_iter_pool_begin();
  INLINE LUIVertexPoolMap::iterator get_iter_pool_end();

  // We store a private root node.
  // With this, we don't have to inherit from LUIObject, but
  // can maintain the ability to attach nodes directly to the
  // root
  PT(LUIObject) _root;

};

#include "luiRoot.I"

#endif
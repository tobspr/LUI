// Filename: luiRoot.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_ROOT_H
#define LUI_ROOT_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "filename.h"
#include "virtualFileSystem.h"

#include "luiVertexPool.h"
#include "luiNode.h"
#include "luiAtlas.h"

#include "config_lui.h"

class LUINode;

class EXPCL_PANDASKEL LUIRoot {

PUBLISHED:

  LUIRoot();
  ~LUIRoot();

  INLINE PT(LUINode) root();

public:

  LUIVertexPool* get_vpool_by_texture(Texture* tex);

private:

  // We store a private root node.
  // With this, we don't have to inherit from LUINode, but
  // can maintain the ability to attach nodes directly to the
  // root
  PT(LUINode) _root;

};

#include "luiRoot.I"

#endif
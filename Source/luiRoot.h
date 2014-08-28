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

#include "config_lui.h"

class LUIRoot {

  PUBLISHED:

    LUIRoot();
    ~LUIRoot();
		
  public:


    LUIVertexPool* get_vpool_by_texture(Texture* tex);
    
	private:

     // todo


};

#endif


#include "luiSprite.h"


LUISprite::LUISprite() : 
  _size(0), 
  _texcoord_start(0), 
  _texcoord_end(1),
  _visible(true), 
  _pool_slot(-1), 
  _vertex_pool(NULL) {  

    for (int i = 0; i < 4; i++) {
      _data[i].x = 0.0;
      _data[i].y = 0.0;
      _data[i].z = 0.0;
      _data[i].u = 0.0;
      _data[i].v = 0.0;
      _data[i].col[0] = 0;
      _data[i].col[1] = 0;
      _data[i].col[2] = 0;
      _data[i].col[3] = 0;
    }

    lui_cat.spam() << "Constructed new LUISprite\n";

}

LUISprite::~LUISprite() {}

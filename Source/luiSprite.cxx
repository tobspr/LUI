

#include "luiSprite.h"


LUISprite::LUISprite() : 
  _size(0), 
  _texcoord_start(0), 
  _texcoord_end(1),
  _visible(true), 
  _pool_slot(-1), 
  _vertex_pool(NULL) {  
}

LUISprite::~LUISprite() {}

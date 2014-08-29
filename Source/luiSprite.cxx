

#include "luiSprite.h"


LUISprite::LUISprite() : 
  _visible(true), 
  _pool_slot(-1), 
  _vertex_pool(NULL) {  

    set_pos(0, 0);
    set_texcoord_start(0, 0);
    set_texcoord_end(1, 1);
    set_size(10, 10);
    set_color(1.0, 1.0, 1.0, 1.0);

    lui_cat.info() << "Constructed new LUISprite\n";
}

LUISprite::~LUISprite() {}

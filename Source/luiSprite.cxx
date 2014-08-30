

#include "luiSprite.h"

LUISprite::LUISprite(LUINode* parent) : 
  LUIBaseElement(),
  _pool_slot(-1), 
  _vertex_pool(NULL),


{  

    lui_cat.spam() << "Constructed new LUISprite\n";

    set_top_left(0, 0);
    set_texcoord_start(0, 0);
    set_texcoord_end(1, 1);
    set_size(10, 10);
    set_color(1.0, 1.0, 1.0, 1.0);

    
}

LUISprite::~LUISprite() {
  lui_cat.spam() << "Destructed a LUISprite\n";
}

void LUISprite::on_position_changed() {
}
void LUISprite::on_size_changed() {
}
void LUISprite::on_visibility_changed() {
}


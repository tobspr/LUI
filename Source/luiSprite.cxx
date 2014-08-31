

#include "luiSprite.h"


int LUISprite::_instance_count = 0;


LUISprite::LUISprite(LUIBaseElement* parent) : 
  LUIBaseElement(),
  _pool_slot(-1), 
  _vertex_pool(NULL)
{  

  _instance_count ++;

  if (lui_cat.is_spam() && lui_cat.is_spam()) {
    cout << "Constructed new LUISprite, (active: " << _instance_count << ")" << endl;  
  }

  set_parent(parent);
  set_top_left(0, 0);
  set_texcoord_start(0, 0);
  set_texcoord_end(1, 1);
  set_size(10, 10);
  set_color(1.0, 1.0, 1.0, 1.0);   
}

LUISprite::~LUISprite() {
  if (lui_cat.is_spam() && lui_cat.is_spam()) {
    _instance_count --;
    cout << "Destructed LUISprite, (left: " << _instance_count << ")" << endl;  
  }
}

void LUISprite::on_bounds_changed() {
  _data[0].x = _pos_x;
  _data[0].y = _pos_y;
  recompute_vertices();
}

void LUISprite::on_visibility_changed() {

}


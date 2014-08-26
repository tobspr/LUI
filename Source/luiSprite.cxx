

#include "luiSprite.h"


LUISprite::LUISprite() : _pos(0), 
  _size(0), _texcoord_start(0), _texcoord_end(1),
  _color(1), _z_index(1.0), _visible(true) {
  
}
LUISprite::~LUISprite() {}
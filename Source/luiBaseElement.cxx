
#include "luiBaseElement.h"

LUIBaseElement::LUIBaseElement() :   
  _visible(true), 
  _offset_x(0),
  _offset_y(0),
  _pos_x(0),
  _pos_y(0),
  _stick_top(true),
  _stick_left(true),
  _size(0),
  _parent(NULL)
{
}

LUIBaseElement::~LUIBaseElement() {
}



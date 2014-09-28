
#include "luiBounds.h"


LUIBounds::LUIBounds(const LVector4 &bounds) : _bounds(bounds) {

}

LUIBounds::LUIBounds(float top, float right, float bottom, float left) : _bounds(top, right, bottom, left) {

}

LUIBounds::~LUIBounds() {

}



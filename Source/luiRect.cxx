
#include "luiRect.h"


LUIRect::LUIRect(const LVector4 &rect) : _rect(rect) {

}

LUIRect::LUIRect(float x, float y, float w, float h) : _rect(x, y, w, h) {

}

LUIRect::~LUIRect() {

}

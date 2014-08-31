

#include "luiVertexPool.h"
LUIVertexPool::LUIVertexPool(Texture *tex) : _tex(tex) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new LUIVertex pool" << endl;
  }

}

LUIVertexPool::~LUIVertexPool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed LUIVertex pool" << endl;
  }

}
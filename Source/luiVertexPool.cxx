

#include "luiVertexPool.h"

LUIVertexPool::LUIVertexPool(Texture *tex) : 
  _tex(tex)
{
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new LUIVertex pool" << endl;
  }

}

LUIVertexPool::~LUIVertexPool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructing LUIVertex pool" << endl;
  }

  for (int i = 0; i < _chunks.size(); i++) {
    delete _chunks[i];
  }
  _chunks.clear();

}

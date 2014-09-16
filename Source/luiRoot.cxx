
#include "luiRoot.h"


LUIRoot::LUIRoot(float width, float height) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructing new LUIRoot ..\n";
  }
  _root = new LUIObject(0.0, 0.0, width, height);
  _root->set_root(this);

}

LUIRoot::~LUIRoot() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed LUIRoot\n";
  }

  // Destruct all LUIVertexPools stored in _pools, as they are not
  // reference counted ..
  for(LUIVertexPoolMap::iterator iter = _pools.begin(); iter != _pools.end(); ++iter)
  {
    LUIVertexPool* pool =  iter->second;
    delete pool;
  }
  _pools.clear();

}

INLINE LUIVertexPoolMap::iterator LUIRoot::get_iter_pool_begin() {
  return _pools.begin();
}

INLINE LUIVertexPoolMap::iterator LUIRoot::get_iter_pool_end() {
  return _pools.end();
}
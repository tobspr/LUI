

INLINE PT(LUIObject) LUIRoot::node() {
  return _root;
}


INLINE LUIVertexPool* LUIRoot::get_vpool_by_texture(Texture* tex) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Finding vertex pool for texture " << tex << endl;
  }

  if (_pools.count(tex) != 0) {

    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Vertex pool found, returning .." << endl;
    }
    return _pools[tex];
  }

  if (lui_cat.is_info()) {
    lui_cat.info() << "Allocating new vertex pool .." << endl;
  }
  LUIVertexPool* pool = new LUIVertexPool(tex);
  _pools[tex] = pool;
  return pool;
}

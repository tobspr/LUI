
// #include "luiBaseElement.h"

INLINE PT(LUIObject) LUIRoot::node() {
  return _root;
}


INLINE LUIVertexPoolMap::iterator LUIRoot::get_iter_pool_begin() {
  return _pools.begin();
}

INLINE LUIVertexPoolMap::iterator LUIRoot::get_iter_pool_end() {
  return _pools.end();
}



INLINE LUIEventObjectSet::iterator LUIRoot::get_event_objects_begin() {
  return _event_objects.begin();
}

INLINE LUIEventObjectSet::iterator LUIRoot::get_event_objects_end() {
  return _event_objects.end();
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

INLINE void LUIRoot::register_event_object(LUIBaseElement *event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Registering event object .." << endl;
    _event_objects.insert(event_object);
  }
}

INLINE void LUIRoot::unregister_event_object(LUIBaseElement *event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Unregistering event object .." << endl;
    _event_objects.erase(event_object);
  }
}
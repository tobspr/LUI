// Filename: luiRoot.h
// Created by:  tobspr (28Aug14)
//

#ifndef LUI_ROOT_H
#define LUI_ROOT_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "config_lui.h"
#include "luiBaseElement.h"
#include "luiObject.h"
#include "luiVertexPool.h"
#include "luiAtlas.h"

class LUIObject;
class LUIBaseElement;

typedef pmap<Texture*, LUIVertexPool*> LUIVertexPoolMap;
typedef set<LUIBaseElement*> LUIEventObjectSet;

class EXPCL_LUI LUIRoot : public ReferenceCount {

  friend class LUIRegion;

PUBLISHED:

  LUIRoot(float width, float height);
  ~LUIRoot();

  INLINE PT(LUIObject) node();

public:

  INLINE LUIVertexPool* get_vpool_by_texture(Texture* tex);

  INLINE void register_event_object(LUIBaseElement *event_object);
  INLINE void unregister_event_object(LUIBaseElement *event_object);


  INLINE void request_focus(LUIBaseElement *elem);
  INLINE LUIBaseElement *get_requested_focus();

  // We expose this to LUIRegion only, so it can iterate over all pools
  // in a fast way.
  INLINE LUIVertexPoolMap::iterator get_iter_pool_begin();
  INLINE LUIVertexPoolMap::iterator get_iter_pool_end();

  INLINE LUIEventObjectSet::iterator get_event_objects_begin();
  INLINE LUIEventObjectSet::iterator get_event_objects_end();


private:



  // Vertex pools are stored as single pointers, to avoid circular
  // references. The destructor of LUIRoot takes care of deleting them.
  LUIVertexPoolMap _pools;


  // We store a private root node.
  // With this, we don't have to inherit from LUIObject, but
  // can maintain the ability to attach nodes directly to the
  // root
  PT(LUIObject) _root;

  // Event objects are not stored reference counted, it is expected that the
  // LUIBaseElement unregisters before destruction.
  LUIEventObjectSet _event_objects;

  // Store the focus requests
  LUIBaseElement* _requested_focus;

};

#include "luiRoot.I"

#endif
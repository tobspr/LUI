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

#include "geomVertexFormat.h"
#include "geomVertexData.h"
#include "geomVertexWriter.h"
#include "geomVertexArrayFormat.h"
#include "geomTriangles.h"
#include "omniBoundingVolume.h"
#include "geom.h"


class LUIObject;
class LUIBaseElement;

typedef vector<Texture*> LUITextureVector;
typedef vector<LUISprite*> LUISpriteVector;
typedef set<LUIBaseElement*> LUIEventObjectSet;

class EXPCL_LUI LUIRoot : public ReferenceCount {

  friend class LUIRegion;

PUBLISHED:

  LUIRoot(float width, float height);
  ~LUIRoot();

  INLINE PT(LUIObject) node();

public:

  INLINE int get_index_by_texture(Texture* tex);

  INLINE void register_event_object(LUIBaseElement *event_object);
  INLINE void unregister_event_object(LUIBaseElement *event_object);

  INLINE void request_focus(LUIBaseElement *elem);
  INLINE LUIBaseElement *get_requested_focus();

  INLINE LUIEventObjectSet::iterator get_event_objects_begin();
  INLINE LUIEventObjectSet::iterator get_event_objects_end();

  INLINE int register_sprite(LUISprite* sprite);
  INLINE void unregister_sprite(int position);

  INLINE void* get_sprite_vertex_pointer(int position);
  INLINE void add_sprite_to_render_list(int position);
  
  INLINE int allocate_render_index();

  INLINE Geom* get_geom();

  INLINE void prepare_render();
  INLINE int get_frame_index();

  INLINE int get_num_textures();
  INLINE Texture *get_texture(int index);

  PT(Shader) create_object_shader();

private:


  PT(GeomVertexData) _vertex_data;
  PT(GeomTriangles) _triangles;
  PT(Geom) _geom;

  LUISpriteVector _sprites;  
  LUITextureVector _textures;

  int _sprites_rendered;
  int _frame_count;
  int _render_index;

  struct LUITriangleIndex {
    uint vertices[3];
  };

  void* _sprite_vertex_pointer;

  int _min_rendered_vertex;
  int _max_rendered_vertex;

  LUITriangleIndex* _triangle_index_buffer;
  int _index_buffer_size;

  vector<int> _topmost_sprites;
  
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
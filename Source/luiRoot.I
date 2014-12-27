
// #include "luiBaseElement.h"

INLINE PT(LUIObject) LUIRoot::node() {
  return _root;
}

INLINE LUIEventObjectSet::iterator LUIRoot::get_event_objects_begin() {
  return _event_objects.begin();
}

INLINE LUIEventObjectSet::iterator LUIRoot::get_event_objects_end() {
  return _event_objects.end();
}

INLINE int LUIRoot::get_index_by_texture(Texture* tex) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Finding vertex pool for texture " << tex << endl;
  }

  nassertr(tex != NULL, -1);

  LUITextureVector::iterator index = std::find(_textures.begin(), _textures.end(), tex);

  if (index != _textures.end()) {

    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Texture index found, returning .." << endl;
    }
    return int(std::distance(_textures.begin(), index));
  }

  if (lui_cat.is_debug()) {
    lui_cat.debug() << "Allocating new texture index .." << endl;
  }

  _textures.push_back(tex);
  return _textures.size() - 1;
}

INLINE void LUIRoot::register_event_object(LUIBaseElement *event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Registering event object .." << endl;
  }
  _event_objects.insert(event_object);
}

INLINE void LUIRoot::unregister_event_object(LUIBaseElement *event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Unregistering event object .." << endl;
  }
  _event_objects.erase(event_object);
}

INLINE void LUIRoot::request_focus(LUIBaseElement *elem) {
  nassertv(elem != NULL);
  _requested_focus = elem;
}

INLINE LUIBaseElement *LUIRoot::get_requested_focus() {
  return _requested_focus;
}

INLINE int LUIRoot::register_sprite(LUISprite* sprite) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Registering sprite " << sprite << "" << endl;
  }

  // Check if there is space free
  for(int i = 0; i != _sprites.size(); i++) {
      if (_sprites[i] == NULL) {
        _sprites[i] = sprite;
        return i;
      }
  }

  // If no space is free, push it to the end
  _sprites.push_back(sprite);
  _vertex_data->set_num_rows(_sprites.size() * 4);
  return _sprites.size() - 1;
}

INLINE void LUIRoot::unregister_sprite(int position) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Unregistering sprite at position " << position << "" << endl;
  }

  // A sprite shouldn't have an invalid index
  nassertv(position < _sprites.size() && position >= 0);

  _sprites[position] = NULL;

  // TODO: If this sprite is the last size, make the vector smaller
  // (Strip empty elements from the end)
}

INLINE void* LUIRoot::get_sprite_vertex_pointer(int position) {
  // A sprite shouldn't have an invalid index
  nassertr(position < _sprites.size() && position >= 0, 0);

  // At the position there should be an actual sprite
  nassertr(_sprites[position] != NULL, 0);

  nassertr(_sprite_vertex_pointer != NULL, 0);

  // nassertr(_sprite_vertex_pointer == _vertex_data->modify_array(0)->modify_handle()->get_write_pointer(), 0);

  return (unsigned char*)_sprite_vertex_pointer + position * sizeof(LUIVertexData) * 4;
}

INLINE void LUIRoot::add_sprite_to_render_list(int position) {

  int pos = position * 4;
  int index = _sprites_rendered * 2;

  // If this triggers, we have a buffer overflow
  // Increase _index_buffer_size to fix this error
  nassertv(index+1 < _index_buffer_size);

  _sprites_rendered++;

  _triangle_index_buffer[index].vertices[0] = pos + 2;
  _triangle_index_buffer[index].vertices[1] = pos + 1;
  _triangle_index_buffer[index].vertices[2] = pos + 0;

  _triangle_index_buffer[index+1].vertices[0] = pos + 3;
  _triangle_index_buffer[index+1].vertices[1] = pos + 2;
  _triangle_index_buffer[index+1].vertices[2] = pos + 0;

  if (pos < _min_rendered_vertex) _min_rendered_vertex = pos;
  if (pos+3 > _max_rendered_vertex) _max_rendered_vertex = pos + 3;


}


INLINE Geom* LUIRoot::get_geom() {
  return _geom;
}

INLINE int LUIRoot::get_num_textures() {
  return _textures.size();
}

INLINE Texture* LUIRoot::get_texture(int index) {
  nassertr(index >= 0 && index < _textures.size(), NULL);
  return _textures[index];  
}

INLINE int LUIRoot::get_frame_index() {
  return _frame_count;
}

INLINE int LUIRoot::allocate_render_index() {
  return _render_index++;
}

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

INLINE int LUIRoot::alloc_index_by_texture(Texture* tex) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Finding vertex pool for texture " << tex << endl;
  }

  nassertr(tex != nullptr, -1);

  auto index = std::find(_textures.begin(), _textures.end(), tex);

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

INLINE void LUIRoot::register_event_object(LUIBaseElement* event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Registering event object .." << endl;
  }
  _event_objects.insert(event_object);
}

INLINE void LUIRoot::unregister_event_object(LUIBaseElement* event_object) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Unregistering event object .." << endl;
  }
  _event_objects.erase(event_object);
}

INLINE bool LUIRoot::request_focus(LUIBaseElement* elem) {
  if (_requested_focus)  {
    if (_requested_focus == elem) {
      lui_cat.info() << "Element " << elem->get_debug_name() << " requested focus twice or more in one frame!" << endl;
      return true;
    } else {
      lui_cat.warning() << "Multiple varying focus requests in on frame - can only serve the first one!" << endl;
    }
    return false;
  }
  set_requested_focus(elem);
  return true;
}

INLINE void LUIRoot::set_requested_focus(LUIBaseElement* elem) {
  _requested_focus = elem;
}

INLINE LUIBaseElement* LUIRoot::get_requested_focus() const {
  return _requested_focus;
}

INLINE int LUIRoot::register_sprite(LUISprite* sprite) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Registering sprite " << sprite << "" << endl;
  }

  // Check if there is space free
  for(int i = 0; i != _sprites.size(); i++) {
      if (_sprites[i] == nullptr) {
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

  _sprites[position] = nullptr;

  // TODO: If this sprite is the last size, make the vector smaller
  // (Strip empty elements from the end)
}

INLINE void* LUIRoot::get_sprite_vertex_pointer(int position) const {
  // A sprite shouldn't have an invalid index
  nassertr(position < _sprites.size() && position >= 0, 0);

  // At the position there should be an actual sprite
  nassertr(_sprites[position] != nullptr, 0);
  nassertr(_sprite_vertex_pointer != nullptr, 0);

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
  if (pos + 3 > _max_rendered_vertex) _max_rendered_vertex = pos + 3;
}

INLINE Geom* LUIRoot::get_geom() const {
  return _geom;
}

INLINE int LUIRoot::get_num_textures() const {
  return _textures.size();
}

INLINE Texture* LUIRoot::get_texture(int index) const {
  nassertr(index >= 0 && index < _textures.size(), nullptr);
  return _textures[index];
}

INLINE int LUIRoot::get_frame_index() const {
  return _frame_count;
}

INLINE int LUIRoot::allocate_render_index() {
  return _render_index++;
}

/**
 * @brief Sets whether to use GLSL 1.30 instead of 1.20
 * @details This controls whether GLSL 1.30 is used instead of 1.20. It can
 *   provide a performance benefit although it also bumps the OpenGL requirement.
 *
 * @param use_glsl_130 Whether to use GLSL 1.30
 */
INLINE void LUIRoot::set_use_glsl_130(bool use_glsl_130) {
  _use_glsl_130 = use_glsl_130;
}


/**
 * @brief Requests explicit blur
 * @details This requests to explicitely blur the currently focused element.
 *   Usually elements are only blurred when other elements are focused, however
 *   in some cases it might make sense to blur an element.
 */
INLINE void LUIRoot::request_explicit_blur() {
  request_focus(nullptr);
  _explicit_blur = true;
}

/**
 * @brief Clears the explicit blur
 * @details This clears any explicit blur request
 */
INLINE void LUIRoot::clear_explicit_blur() {
  _explicit_blur = false;
}

/**
 * @brief Returns whether explicit blur was requested
 * @details This returns whether any element requested explicit blur, previously
 *   set with request_explici_tblur()
 */
INLINE bool LUIRoot::get_explicit_blur() const {
  return _explicit_blur;
}

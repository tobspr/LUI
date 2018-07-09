
INLINE bool LUIVertexChunk::is_empty() const {
  return _sprite_count == 0;
}

INLINE bool LUIVertexChunk::has_space() const {
  return _sprite_count < _chunk_size;
}

INLINE Geom* LUIVertexChunk::get_geom() const {
  return _geom;
}

INLINE int LUIVertexChunk::reserve_slot(LUISprite* sprite) {
  nassertr(has_space(), 0);

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Reserving slot .. " <<  endl;
  }

  int slot = -1;
  for (int i = 0; i < _chunk_size; i++) {
    if (_children[i] == nullptr) {
      // found slot
      slot = i;
      break;
    }
  }

  // As we checked for has_space above, this should never happen
  nassertr(slot >= 0 && slot < _chunk_size, 0);

  _children[slot] = sprite;
  _sprite_count ++;

  return slot;
}

INLINE void LUIVertexChunk::free_slot(int slot) {

  nassertv(slot < _chunk_size);
  nassertv(!is_empty());

  if (_children[slot] == nullptr) {
    lui_cat.error() << "Cannot free slot, as it is not used" << endl;
    return;
  }

  _children[slot] = nullptr;
  _sprite_count --;


  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Free slot " << slot << endl;
  }

  for (int i = 0; i < 4; i++) {
    memset(get_slot_ptr(slot), 0, sizeof(LUIVertexData) * 4);
  }


  if (_sprite_count < 1) {
    if (lui_cat.is_spam()) {
      // TODO: Unregister from vertex pool
      lui_cat.debug() << "Detected empty vertex chunk, should be garbarge collected" << endl;
    }
  }
}

INLINE void* LUIVertexChunk::get_slot_ptr(int slot) const {

  // Make sure the write pointer is correct
  nassertr(_vertex_data->modify_array(0)->modify_handle()->get_write_pointer() == _write_pointer, nullptr);

  // Make sure we don't write at the wrong location
  nassertr(slot < _chunk_size, nullptr);

  return (void*)((uintptr_t)_write_pointer + sizeof(LUIVertexData) * 4 * slot);
}

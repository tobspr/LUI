
INLINE bool LUIVertexChunk::is_empty() {
  return _sprite_count == 0;
}

INLINE bool LUIVertexChunk::has_space() {
  return _sprite_count < _chunk_size;
}

INLINE Geom* LUIVertexChunk::get_geom() {
  return _geom;
}

INLINE int LUIVertexChunk::reserve_slot(LUISprite *sprite) {
  cout << "Reserving slot .. " <<  endl;

  nassertr(has_space(), 0); 

  return 0;
}

INLINE void LUIVertexChunk::free_slot(int slot) {

  nassertv(slot < _chunk_size);
  cout << "Free slot " << slot << endl;
}

INLINE void *LUIVertexChunk::get_slot_ptr(int slot) {

  // Make sure the write pointer is correct
  nassertr(_vertex_data->modify_array(0)->modify_handle()->get_write_pointer() == _write_pointer, NULL);
  
  // Make sure we don't write at the wrong location
  nassertr(slot < _chunk_size, NULL);

  return (void*)((uintptr_t)_write_pointer + sizeof(LUIVertexData) * 4 * slot);
}
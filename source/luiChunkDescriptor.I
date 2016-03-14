

INLINE int LUIChunkDescriptor::get_slot() const {
  return _slot;
}
INLINE LUIVertexChunk* LUIChunkDescriptor::get_chunk() const {
  return _chunk;
}

INLINE void LUIChunkDescriptor::set_slot(int slot) {
  _slot = slot;
}
INLINE void LUIChunkDescriptor::set_chunk(LUIVertexChunk* chunk) {
  _chunk = chunk;
}

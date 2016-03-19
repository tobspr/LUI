

INLINE int LUIVertexPool::get_num_chunks() const {
  return _chunks.size();

}
INLINE LUIVertexChunk* LUIVertexPool::get_chunk(int n) const {
  nassertr(n >= 0 && n < _chunks.size(), NULL);
  return _chunks[n];
}

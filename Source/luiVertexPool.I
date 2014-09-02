
  
INLINE int LUIVertexPool::get_num_chunks() {
  return _chunks.size();

}
INLINE LUIVertexChunk* LUIVertexPool::get_chunk(int n) {
  nassertr(n >= 0 && n < _chunks.size(), NULL);
  return _chunks[n];
}
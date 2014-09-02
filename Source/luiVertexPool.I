
INLINE LUIChunkDescriptor *LUIVertexPool::allocate_slot(LUISprite* child) {
  LUIChunkDescriptor *result = new LUIChunkDescriptor();
  result->set_chunk(NULL);
  result->set_slot(0);
  return result;
}




#include "luiVertexPool.h"

LUIVertexPool::LUIVertexPool(Texture* tex) :
  _tex(tex)
{
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new LUIVertex pool" << endl;
  }

}

LUIVertexPool::~LUIVertexPool() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructing LUIVertex pool" << endl;
  }

  for (int i = 0; i < _chunks.size(); i++) {
    delete _chunks[i];
  }
  _chunks.clear();

}

LUIChunkDescriptor* LUIVertexPool::allocate_slot(LUISprite* child) {

  LUIVertexChunk* chunk = nullptr;

  for (int i = 0; i < _chunks.size(); i++) {
    LUIVertexChunk* current = _chunks[i];
    if (current->has_space()) {
      chunk = current;
      break;
    }
  }

  if (chunk == nullptr) {
    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Allocating new lui vertex chunk .." << endl;
    }
    allocate_chunk();
    chunk = _chunks.back();
  } else {
    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Found chunk at " << chunk << endl;
    }
  }

  // At this place, the chunk should not be nullptr. Either we allocated a new one,
  // or we took an existing one, but in all cases we have one.
  nassertr(chunk != nullptr, nullptr);

  int slot = chunk->reserve_slot(child);
  nassertr(slot >= 0, nullptr);

  LUIChunkDescriptor* result = new LUIChunkDescriptor();
  result->set_chunk(chunk);
  result->set_slot(slot);
  return result;
}

void LUIVertexPool::allocate_chunk() {
  LUIVertexChunk* chunk = new LUIVertexChunk(10000);
  _chunks.push_back(chunk);
}

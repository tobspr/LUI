
#include "luiChunkDescriptor.h"
#include "luiVertexChunk.h"

void LUIChunkDescriptor::release() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LuiChunkDescriptor: Releasing slot .. " << endl;
  }
  _chunk->free_slot(_slot);
}

void* LUIChunkDescriptor::get_write_ptr() const {
  return _chunk->get_slot_ptr(_slot);
}

LUIChunkDescriptor::LUIChunkDescriptor() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Constructed new chunk descriptor" << endl;
  }
}

LUIChunkDescriptor::~LUIChunkDescriptor() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Destructed chunk descriptor" << endl;
  }
}

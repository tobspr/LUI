
#include "luiChunkDescriptor.h"
#include "luiVertexChunk.h"

void LUIChunkDescriptor::release() {
  if (lui_cat.is_spam()) {
    cout << "LuiChunkDescriptor: Releasing slot .. " << endl;
  }
  _chunk->free_slot(_slot);
}  

void* LUIChunkDescriptor::get_write_ptr() {
  return _chunk->get_slot_ptr(_slot);
}

LUIChunkDescriptor::LUIChunkDescriptor() {
  if (lui_cat.is_spam()) {
    cout << "Constructed new chunk descriptor" << endl;
  }
}

LUIChunkDescriptor::~LUIChunkDescriptor() {
  if (lui_cat.is_spam()) {
    cout << "Destructed chunk descriptor" << endl;
  }
}
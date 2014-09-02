
#include "luiChunkDescriptor.h"
#include "luiVertexChunk.h"

void LUIChunkDescriptor::release() {
  cout << "LuiChunkDescriptor: Releasing slot .. " << endl;
}  

void* LUIChunkDescriptor::get_write_ptr() {
  return _chunk->get_slot_ptr(_slot);
}

LUIChunkDescriptor::LUIChunkDescriptor() {
  cout << "Constructed new chunk descriptor" << endl;
}

LUIChunkDescriptor::~LUIChunkDescriptor() {
  cout << "Destructed chunk descriptor" << endl;
}
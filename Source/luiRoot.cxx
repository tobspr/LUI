
#include "luiRoot.h"


LUIRoot::LUIRoot() {
    lui_cat.spam() << "Initialized new LUIRoot\n";
}
LUIRoot::~LUIRoot() {
  lui_cat.spam() << "Destructed LUIRoot\n";
}

LUIVertexPool* LUIRoot::get_vpool_by_texture(Texture* tex) {
  return NULL;
}


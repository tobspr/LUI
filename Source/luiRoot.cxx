
#include "luiRoot.h"


LUIRoot::LUIRoot() {
    lui_cat.info() << "Initialized new LUIRoot\n";
}
LUIRoot::~LUIRoot() {}

LUIVertexPool* LUIRoot::get_vpool_by_texture(Texture* tex) {
  return NULL;
}

void LUIRoot::operator += (PT(LUINode) node) {
  cout << "Add widget (root, forwarding)" << endl;

  // Not sure if this is correct
  *_root += node;
}

PT(LUISprite) LUIRoot::attach_sprite(float x, float y, LUIAtlasDescriptor desc) {
  return _root->attach_sprite(x, y, desc);
}
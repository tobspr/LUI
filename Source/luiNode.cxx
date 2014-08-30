

#include "luiNode.h"


LUINode::LUINode() {

}

LUINode::~LUINode() {

}

void LUINode::operator += (PT(LUINode) node) {
    cout << "Add widget" << endl;
}

LUIAtlasDescriptor LUINode::get_atlas_image(string identifier) {
  LUIAtlasDescriptor result;
  lui_cat.error() << "Atlas image '" << identifier << " not found!" << endl;
  return result;
}
 
PT(LUISprite) LUINode::attach_sprite(float x, float y, LUIAtlasDescriptor desc) {
  PT(LUISprite) sprite = new LUISprite();
  sprite->set_pos(x, y);
  sprite->set_size(desc.width, desc.height);
  sprite->set_texcoord_start(desc.uv_begin);
  sprite->set_texcoord_end(desc.uv_end);
      
  return sprite;
}

//PT(LUISprite) LUINode::attach_sprite(string identifier) {
// return NULL;
//}



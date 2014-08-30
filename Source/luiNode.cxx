

#include "luiNode.h"


LUINode::LUINode() {
  lui_cat.spam() << "Created a new LUINode" << endl;
}

LUINode::~LUINode() {
  lui_cat.spam() << "Destructed a LUINode" << endl;
}

void LUINode::operator += (PT(LUINode) node) {
  lui_cat.info() << "Addding widget .." << endl;
}

PT(LUIAtlasDescriptor) LUINode::get_atlas_image(const string &identifier) {
  return LUIAtlasPool::get_global_ptr()->get_descriptor("default", identifier);
}

PT(LUIAtlasDescriptor) LUINode::get_atlas_image(const string &atlas_id, const string &identifier) {
  return LUIAtlasPool::get_global_ptr()->get_descriptor(atlas_id, identifier);
}

PT(LUISprite) LUINode::attach_sprite(float x, float y, PT(LUIAtlasDescriptor) desc) {
  lui_cat.info() << "Attach sprite from atlas descriptor" << endl;
  PT(LUISprite) sprite = new LUISprite();
  sprite->set_pos(x, y);
  sprite->set_texture(desc);
  return sprite;
}

PT(LUISprite) LUINode::attach_sprite(float x, float y, const string &source) {
  lui_cat.info() << "Attach sprite from string: '" << source << "'" << endl;
  PT(LUISprite) sprite = new LUISprite();
  sprite->set_pos(x, y);
  sprite->set_texture(source);
  return sprite;
}

//PT(LUISprite) LUINode::attach_sprite(string identifier) {
// return NULL;
//}



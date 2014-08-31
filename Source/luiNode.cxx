

#include "luiNode.h"


LUINode::LUINode(float w, float h) : LUIBaseElement() {
  set_size(w, h);
  lui_cat.spam() << "Created a new LUINode" << endl;
}

LUINode::~LUINode() {
  lui_cat.spam() << "Destructing a LUINode, removing all sprites" << endl;

  _sprites.clear();
  _nodes.clear();
}

void LUINode::operator += (PT(LUINode) node) {
  lui_cat.info() << "Addding widget .." << endl;
}


void LUINode::on_bounds_changed() {
  refresh_sprite_positions();
}


void LUINode::on_visibility_changed() {

}


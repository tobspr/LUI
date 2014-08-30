

#include "luiNode.h"


LUINode::LUINode() {
  lui_cat.spam() << "Created a new LUINode" << endl;
}

LUINode::~LUINode() {
  lui_cat.spam() << "Destructing a LUINode, removing all sprites" << endl;

  while (_sprites.size() > 0) {
    remove_sprite(_sprites[0]);
  }
  _sprites.clear();
  _nodes.clear();
}

void LUINode::operator += (PT(LUINode) node) {
  lui_cat.info() << "Addding widget .." << endl;
}

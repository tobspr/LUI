

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

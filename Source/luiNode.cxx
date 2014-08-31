

#include "luiNode.h"


int LUINode::_instance_count = 0;

LUINode::LUINode(float w, float h) : LUIBaseElement() {
  set_size(w, h);

  _instance_count ++;
  if (lui_cat.is_spam()) {
    cout << "Created a new LUINode (active instances: " << _instance_count << ")" << endl;
  }
}

LUINode::~LUINode() {

  _instance_count --;
  if (lui_cat.is_spam()) {
    cout << "Destructing LUINode, instances left: " << _instance_count << endl;
  }

  _sprites.clear();
  _nodes.clear();
}


void LUINode::on_bounds_changed() {
  refresh_child_positions();
}


void LUINode::on_visibility_changed() {
  refresh_child_visibility();
}

void LUINode::set_root(LUIRoot* root) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUINode - root changed" << endl;
  }

  if (_root != NULL && root != _root) {
    lui_cat.error() << "Node already has a root!" << endl;
    return;
  }

  if (root != _root) {
    _root = root;

    if (lui_cat.is_spam()) {
      lui_cat.spam() << "Refreshing child root .. " << endl;
    }

    // Update sprites
    for (int i = 0; i < _sprites.size(); i++) {
      _sprites[i]->set_root(root);
    }  

    // Updates nodes
    for (int i = 0; i < _nodes.size(); i ++) {
      _nodes[i]->set_root(root);
    }
  }
}

void LUINode::on_detached() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUINode got detached" << endl;
  }
  _root = NULL;
  _parent = NULL;

  // Update sprites
  for (int i = 0; i < _sprites.size(); i++) {
    _sprites[i]->on_detached();
  }  

  // Updates nodes
  for (int i = 0; i < _nodes.size(); i ++) {
    _nodes[i]->on_detached();
  }
}
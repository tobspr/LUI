

#include "luiObject.h"


int LUIObject::_instance_count = 0;

LUIObject::LUIObject(float w, float h) : LUIBaseElement() {
  set_size(w, h);

  _instance_count ++;
  if (lui_cat.is_spam()) {
    cout << "Created a new LUIObject (active instances: " << _instance_count << ")" << endl;
  }
}

LUIObject::~LUIObject() {

  _instance_count --;
  if (lui_cat.is_spam()) {
    cout << "Destructing LUIObject, instances left: " << _instance_count << endl;
  }

  _sprites.clear();
  _nodes.clear();
}


void LUIObject::on_bounds_changed() {
  refresh_child_positions();
}


void LUIObject::on_visibility_changed() {
  refresh_child_visibility();
}

void LUIObject::set_root(LUIRoot* root) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUIObject - root changed" << endl;
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

void LUIObject::on_detached() {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "LUIObject got detached" << endl;
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

void LUIObject::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIObject] pos = " << _pos_x << ", " << _pos_y << "; size = " << _size.get_x() << " x " << _size.get_y() << endl;

  // List sprites
  for (int i = 0; i < _sprites.size(); i++) {
    _sprites[i]->ls(indent + 1);
  }  

  // List nodes
  for (int i = 0; i < _nodes.size(); i ++) {
    _nodes[i]->ls(indent + 1);
  }
} 
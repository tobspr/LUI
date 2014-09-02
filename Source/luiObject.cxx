

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

PT(LUISpriteIterator) LUIObject::sprites() {
  return new LUISpriteIterator(_sprites.begin(), _sprites.end());
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
    for (lui_sprite_iterator it = _sprites.begin(); it!= _sprites.end(); ++it) {
      (*it)->set_root(root);
    }

    // Updates nodes
    for (lui_object_iterator it = _nodes.begin(); it!= _nodes.end(); ++it) {
      (*it)->set_root(root);
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
  for (lui_sprite_iterator it = _sprites.begin(); it!= _sprites.end(); ++it) {
    (*it)->on_detached();
  }

  // Updates nodes
  for (lui_object_iterator it = _nodes.begin(); it!= _nodes.end(); ++it) {
    (*it)->on_detached();
  }

}

void LUIObject::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIObject] pos = " << _pos_x << ", " << _pos_y << "; size = " << _size.get_x() << " x " << _size.get_y() << endl;

  // Update sprites
  for (lui_sprite_iterator it = _sprites.begin(); it!= _sprites.end(); ++it) {
    (*it)->ls(indent + 1);
  }

  // Updates nodes
  for (lui_object_iterator it = _nodes.begin(); it!= _nodes.end(); ++it) {
    (*it)->ls(indent + 1);
  }
} 
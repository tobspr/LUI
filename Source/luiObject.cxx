

#include "luiObject.h"


TypeHandle LUIObject::_type_handle;

NotifyCategoryDef(luiObject, ":lui");

int LUIObject::_instance_count = 0;


LUIObject::LUIObject(float x, float y, float w, float h) : LUIBaseElement() {
  init();

   // Prevent recomputation of the position while we initialize the object
  begin_update_section();
  
  set_size(w, h);
  set_pos(x, y);

  end_update_section();

}

LUIObject::LUIObject(LUIObject *parent, float x, float y, float w, float h)  : LUIBaseElement() {
  init();

  // Prevent recomputation of the position while we initialize the object
  begin_update_section();
  set_size(w, h);
  set_pos(x, y);

  parent->add_child(this);
  
  end_update_section();

}

LUIObject::~LUIObject() {

  _instance_count --;
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Destructing LUIObject, instances left: " << _instance_count << endl;
  }

  _children.clear();
}

void LUIObject::init() {
  _instance_count ++;
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Constructing new LUIObject (active: " << _instance_count << ")" << endl;
  }
}

PT(LUIElementIterator) LUIObject::children() {
  return new LUIElementIterator(_children.begin(), _children.end());
}

void LUIObject::on_bounds_changed() {
  refresh_child_positions();
}

void LUIObject::on_visibility_changed() {
  refresh_child_visibility();
}

void LUIObject::on_z_index_changed() {
  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->recompute_z_index();
  }
}

void LUIObject::set_root(LUIRoot* root) {

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Root changed" << endl;
  }

  if (_root != NULL && root != _root) {
    luiObject_cat.error() << "Object is already attached to another root!" << endl;
    return;
  }

  if (root != _root) {

    // Unregister from old root
    unregister_events();
    _root = root;

    // Register to new root
    register_events();

    for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
      (*it)->set_root(_root);
    }

  }
}

void LUIObject::on_detached() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Got detached .." << endl;
  }

  unregister_events();
  _root = NULL;
  _parent = NULL;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_detached();
  }

}

void LUIObject::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIObject] pos = " << _pos_x << ", " << _pos_y << "; size = " << _size.get_x() << " x " << _size.get_y() << "; z-index = " << _z_index << " (+ "<< _local_z_index << ")" << endl;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
   (*it)->ls(indent + 1);
  }

} 
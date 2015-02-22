
#include "luiObject.h"

NotifyCategoryDef(luiObject, ":lui");

int LUIObject::_instance_count = 0;
TypeHandle LUIObject::_type_handle;

LUIObject::LUIObject(PyObject *self, float x, float y, float w, float h, bool solid) : LUIBaseElement(self) {
  init();
  begin_update_section();
  _size.set_x(w);
  _size.set_y(h);
  set_pos(x, y);
  set_solid(solid);
  end_update_section();
}

LUIObject::LUIObject(PyObject *self, LUIObject *parent, float x, float y, float w, float h, bool solid)  : LUIBaseElement(self) {
  init();

  // Prevent recomputation of the position while we initialize the object
  begin_update_section();
  _size.set_x(w);
  _size.set_y(h);
  set_pos(x, y);
  set_solid(solid);
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
  _sort_children = true;
  _content_node = NULL;
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Constructing new LUIObject (active: " << _instance_count << ")" << endl;
  }
}


void LUIObject::set_root(LUIRoot* root) {
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

void LUIObject::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIObject] pos = " << _pos_x << ", " << _pos_y << "; size = " << _size.get_x() << " x " << _size.get_y() << "; z = " << _z_offset << endl;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
   (*it)->ls(indent + 1);
  }
} 



INLINE bool lui_compare_z_offset(LUIBaseElement* a, LUIBaseElement* b) {
  return a->get_z_offset() < b->get_z_offset();
}

void LUIObject::render_recursive(bool is_topmost_pass, bool render_anyway) {

  if (!_visible) return;

  bool do_render = false;
  bool do_render_children = false;
  bool do_render_anyway = false;

  if (!is_topmost_pass) {
    do_render = is_topmost_pass == _topmost;
    do_render_children = do_render;
    do_render_anyway = false;
  } else {
    do_render = is_topmost_pass == _topmost || render_anyway;
    do_render_children = true;
    do_render_anyway = do_render_anyway || do_render;
  }

  
  nassertv(_root != NULL);

  if (do_render) {
    _last_frame_visible = _root->get_frame_index();
    recompute_position();
    fetch_render_index();

    // If z-sorting is enabled, sort by z-offset
    if (_sort_children) {
      std::sort(_children.begin(), _children.end(), lui_compare_z_offset);
    }
  }

  // Render all children, sorted by their relative z-index
  if (do_render_children) {
    for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
      (*it)->render_recursive(is_topmost_pass, do_render_anyway);
    }
  }
}
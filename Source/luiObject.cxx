
#include "luiObject.h"
#include "luiRoot.h"

NotifyCategoryDef(luiObject, ":lui");

int LUIObject::_instance_count = 0;
TypeHandle LUIObject::_type_handle;

LUIObject::LUIObject(PyObject *self, float x, float y, float w, float h, bool solid) : LUIBaseElement(self) {
  init();
  begin_update_section();
  set_size(w, h);
  set_pos(x, y);
  set_solid(solid);
  end_update_section();
}

LUIObject::LUIObject(PyObject *self, LUIObject *parent, float x, float y, float w, float h, bool solid)  : LUIBaseElement(self) {
  init();

  // Prevent recomputation of the position while we initialize the object
  begin_update_section();
  set_size(w, h);
  set_pos(x, y);
  set_solid(solid);
  parent->add_child(this);
  end_update_section();
}

LUIObject::~LUIObject() {
  --_instance_count;
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Destructing LUIObject, instances left: " << _instance_count << endl;
  }
  _children.clear();
}

void LUIObject::init() {
  ++_instance_count;
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

    for (auto it = _children.begin(); it!= _children.end(); ++it) {
      (*it)->set_root(_root);
    }
  }
}

void LUIObject::ls(int indent) {
  cout << string(indent, ' ')  << "[LUIObject] pos = " << _pos_x << ", " << _pos_y << "; size = "
       << get_height() << " x " << get_width() << "; z = " << _z_offset << endl;

  for (auto it = _children.cbegin(); it != _children.cend(); ++it) {
   (*it)->ls(indent + 1);
  }
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
    fetch_render_index();
  }

  // Render all children, sorted by their relative z-index
  if (do_render_children) {
    for (auto it = _children.begin(); it!= _children.end(); ++it) {
      (*it)->render_recursive(is_topmost_pass, do_render_anyway);
    }
  }
}

INLINE void LUIObject::update_dimensions() {

  // if (_parent) {
  //   cout << "Updating dimensions .. parent size is: " << _parent->get_size() << endl;
  // } else {
  //   cout << "Updating dimensions .. no parent" << endl;
  // }

  // When the user set a size on the container, like 10px or 50%
  if (_size_x.has_expression()) {
    if (_parent) {
      _effective_size.set_x(_size_x.evaluate(_parent->get_width()));
    } else {
      _effective_size.set_x(_size_x.evaluate(0));
    }

  // Otherwise fit the container arround its childrens
  } else {
    float max_x = get_abs_pos().get_x();

    // Find the maximum children extent
    for (auto it = _children.begin(); it != _children.end(); ++it) {
      LUIBaseElement *elem = *it;
      if (elem->contributes_to_fluid_width()) {
        max_x = max(max_x, elem->get_x_extent());
      }
    }
    max_x -= get_abs_pos().get_x();
    max_x -= _padding.get_left() + _padding.get_right();
    _effective_size.set_x(max_x);
  }

  // When the user set a size on the container, like 10px or 50%
  if (_size_y.has_expression()) {
    if (_parent) {
      _effective_size.set_y(_size_y.evaluate(_parent->get_height()));
    } else {
      _effective_size.set_y(_size_y.evaluate(0));
    }

  // Otherwise fit the container arround its childrens
  } else {
    float max_y = get_abs_pos().get_y();

    // Find the maximum children extent
    for (auto it = _children.begin(); it != _children.end(); ++it) {
      LUIBaseElement *elem = *it;
      if (elem->contributes_to_fluid_height()) {
        max_y = max(max_y, elem->get_y_extent());
      }
    }
    max_y -= get_abs_pos().get_y();
    max_y -= _padding.get_top() + _padding.get_bottom();
    _effective_size.set_y(max_y);
  }

  // cout << "Updated position, new effective size is " << _effective_size << endl;
}

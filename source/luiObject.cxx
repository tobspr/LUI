
#include "luiObject.h"
#include "luiRoot.h"

NotifyCategoryDef(luiObject, ":lui");

int LUIObject::_instance_count = 0;
TypeHandle LUIObject::_type_handle;

LUIObject::LUIObject(PyObject* self, float x, float y, float w, float h, bool solid)
  : LUIBaseElement(self) {
  init();
  set_size(w, h);
  set_pos(x, y);
  set_solid(solid);
}

LUIObject::LUIObject(PyObject* self, LUIObject* parent, float x, float y, float w, float h, bool solid)
  : LUIBaseElement(self) {
  init();
  set_size(w, h);
  set_pos(x, y);
  set_solid(solid);
  parent->add_child(this);
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
  _content_node = nullptr;
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Constructing new LUIObject (active: " << _instance_count << ")" << endl;
  }
}

void LUIObject::set_root(LUIRoot* root) {
  if (_root != nullptr && root != _root) {
    luiObject_cat.error() << "Object is already attached to another root! target = " << _debug_name << endl;
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
  cout << string(indent, ' ')  << "[" << _debug_name << "] pos = " << get_abs_pos().get_x() << ", " << get_abs_pos().get_y() << "; size = "
       << get_width() << " x " << get_height() << "; z = " << _z_offset << endl;

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

  nassertv(_root != nullptr);

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
  LVector2 available_dimensions = get_available_dimensions();
  if (_size.x.has_expression())
    _effective_size.set_x(_size.x.evaluate(available_dimensions.get_x()));
  if (_size.y.has_expression())
    _effective_size.set_y(_size.y.evaluate(available_dimensions.get_y()));

}

void LUIObject::fit_dimensions() {

  // Update the dimensions for all expresions which require information about
  // the children elements.

  if (!_size.x.has_expression()) {
    float max_x = _abs_position.get_x();

    // Find the maximum children extent
    for (auto it = _children.begin(); it != _children.end(); ++it) {
      LUIBaseElement* elem = *it;
      if (elem->_placement.x == M_default && !elem->_size.x.has_parent_dependent_expression()) {
        max_x = max(max_x, elem->get_x_extent());
      }
    }

    // Get the relative size
    max_x -= _abs_position.get_x();

    // Take padding into account
    max_x += _padding.get_right();

    if (_snap_position) max_x = ceil(max_x);
    _effective_size.set_x(max_x);
  }

  if (!_size.y.has_expression()) {
    float max_y = _abs_position.get_y();

    // Find the maximum children extent
    for (auto it = _children.begin(); it != _children.end(); ++it) {
      LUIBaseElement* elem = *it;
      if (elem->_placement.y == M_default && !elem->_size.y.has_parent_dependent_expression()) {
        max_y = max(max_y, elem->get_y_extent());
      }
    }

    // Get the relative size
    max_y -= _abs_position.get_y();

    // Take padding into account
    max_y += _padding.get_bottom();

    if (_snap_position) max_y = ceil(max_y);
    _effective_size.set_y(max_y);
  }

}

void LUIObject::update_dimensions_upstream() {

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->update_dimensions_upstream();
  }

  fit_dimensions();
  update_dimensions();
}

void LUIObject::update_downstream() {
  LUIBaseElement::update_downstream();
  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->update_downstream();
  }
}

void LUIObject::update_upstream() {
  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->update_upstream();
  }
  LUIBaseElement::update_upstream();
}

void LUIObject::update_clip_bounds() {
  LUIBaseElement::update_clip_bounds();
  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->update_clip_bounds();
  }
}

void LUIObject::move_by(const LVector2& offset) {
  LUIBaseElement::move_by(offset);
  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->move_by(offset);
  }
}

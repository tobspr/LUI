
INLINE bool lui_compare_z_offset(LUIBaseElement* a, LUIBaseElement* b) {
  return a->get_z_offset() < b->get_z_offset();
}

INLINE void LUIObject::remove_child(PT(LUIBaseElement) child) {

  if (_content_node) {
    return _content_node->remove_child(child);
  }

  auto child_it = std::find(_children.cbegin(), _children.cend(), child);

  if (child_it == _children.end()) {
    luiObject_cat.warning() << "Attempted to remove child, but child is not attached to this object" << endl;
    return;
  }

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing child .." << endl;
  }

  _children.erase(child_it);
  child->on_detached();
  child->do_set_parent(NULL);

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Reference count is now: " << child->get_ref_count() << endl;
  }
}

INLINE void LUIObject::on_child_z_offset_changed() {
  if (!std::is_sorted(_children.cbegin(), _children.cend(), lui_compare_z_offset))
    std::sort(_children.begin(), _children.end(), lui_compare_z_offset);
}

INLINE void LUIObject::remove_all_children() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing all children .." << endl;
  }

  // Detach all children
  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->on_detached();
    (*it)->do_set_parent(NULL);
  }

  // Now clear the vector
  _children.clear();
}


INLINE PT(LUIBaseElement) LUIObject::add_child(PT(LUIBaseElement) child) {
  if (_content_node) {
    return _content_node->add_child(child);
  }

  if (child->get_parent()) {
    luiObject_cat.error() << "You cannot reattach a child, unattach the child from it's current parent first" << endl;
    return child;
  }

  child->do_set_parent(this);
  child->recompute_position();
  child->on_color_changed();
  _children.push_back(child);

  // This has to be last. Otherwise we're attaching to the pool with outdated positions
  child->set_root(_root);

  on_child_z_offset_changed();

  return child;
}

INLINE PT(LUIElementIterator) LUIObject::get_children() const {
  return new LUIElementIterator(_children.begin(), _children.end());
}

INLINE PT(LUIBaseElement) LUIObject::get_child(size_t index) const {
  nassertr(index < _children.size(), NULL);
  return _children[index];
}

INLINE int LUIObject::get_child_count() const {
  return _children.size();
}

INLINE void LUIObject::on_color_changed() {
  LUIBaseElement::on_color_changed();
  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_color_changed();
  }
}

INLINE void LUIObject::on_bounds_changed() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Updating children .. " << endl;
  }

  for (auto it = _children.begin(); it != _children.end(); ++it) {
    (*it)->recompute_position();
  }
}

INLINE void LUIObject::on_detached() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Got detached .." << endl;
  }

  unregister_events();
  _root = NULL;
  _parent = NULL;

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_detached();
  }
}

INLINE void LUIObject::fit_to_children() {

  float max_x = 0;
  float max_y = 0;

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());

    if (child->_placement_x == M_default) {
      max_x = max(max_x, pos.get_x() + child->get_width());
    }

    if (child->_placement_y == M_default) {
      max_y = max(max_y, pos.get_y() + child->get_height());
    }
  }

  max_x = max(get_padding_left(), max_x);
  max_y = max(get_padding_top(), max_y);

  set_size(max_x + get_padding_right(), max_y + get_padding_bottom());
}

INLINE void LUIObject::fit_height_to_children() {
  float max_y = 0;

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());
    if (child->_placement_y == M_default) {
      max_y = max(max_y, pos.get_y() + child->get_height());
    }
  }
  max_y = max(get_padding_top(), max_y);
  set_height(max_y + get_padding_bottom());
}

INLINE void LUIObject::fit_width_to_children() {
  float max_x = 0;

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());
    if (child->_placement_x == M_default) {
      max_x = max(max_x, pos.get_x() + child->get_width());
    }
  }
  max_x = max(get_padding_left(), max_x);
  set_height(max_x + get_padding_right());
}

INLINE void LUIObject::set_content_node(PT(LUIObject) content_node) {
  _content_node = content_node;
}

INLINE PT(LUIObject) LUIObject::get_content_node() const {
  return _content_node;
}

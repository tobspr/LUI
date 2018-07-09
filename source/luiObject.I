
INLINE bool lui_compare_z_offset(LUIBaseElement* a, LUIBaseElement* b) {
  return a->get_z_offset() < b->get_z_offset();
}

INLINE void LUIObject::remove_child(PT(LUIBaseElement) child) {

  if (_content_node) {
    return _content_node->remove_child(child);
  }

  auto child_it = std::find(_children.begin(), _children.end(), child);

  if (child_it == _children.end()) {
    luiObject_cat.warning() << "Attempted to remove child, but child is not attached to this object. Parent = " << _debug_name << ", child = " << child->_debug_name << endl;
    return;
  }

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing child .." << endl;
  }

  _children.erase(child_it);
  child->on_detached();
  child->do_set_parent(nullptr);

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
    (*it)->do_set_parent(nullptr);
  }

  // Now clear the vector
  _children.clear();
}


INLINE PT(LUIBaseElement) LUIObject::add_child(PT(LUIBaseElement) child) {
  if (_content_node) {
    return _content_node->add_child(child);
  }

  if (child->get_parent()) {
    luiObject_cat.error() << "You cannot reattach a child, unattach the child from it's current parent first! target = " << child->_debug_name << endl;
    return child;
  }

  child->do_set_parent(this);
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
  nassertr(index < _children.size(), nullptr);
  return _children[index];
}

INLINE int LUIObject::get_child_count() const {
  return _children.size();
}

INLINE void LUIObject::on_detached() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Got detached .." << endl;
  }

  unregister_events();
  _root = nullptr;
  _parent = nullptr;

  for (auto it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_detached();
  }
}

INLINE void LUIObject::set_content_node(PT(LUIObject) content_node) {
  _content_node = content_node;
}

INLINE PT(LUIObject) LUIObject::get_content_node() const {
  return _content_node;
}

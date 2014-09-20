
INLINE void LUIObject::remove_child(PT(LUIBaseElement) child) {
  if (find(_children.begin(), _children.end(), child) == _children.end()) {
    luiObject_cat.warning() << "Attempted to remove child, but child is not attached to this object" << endl;
    return;
  }

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing child .." << endl;
  }

  _children.erase(child);
  child->on_detached();
  
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Reference count is now: " << child->get_ref_count() << endl;
  }
}

INLINE void LUIObject::remove_all_children() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing all children .." << endl;
  }

  // Detach all children
  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_detached();
  }

  // Now clear the set
  _children.clear();
}


INLINE PT(LUIBaseElement) LUIObject::add_child(PT(LUIBaseElement) child) {

  if (child->get_parent() != NULL) {
    luiObject_cat.error() << "You cannot reattach a child, unattach the child from it's current parent first" << endl;
    return child;
  }

  child->set_parent(this);
  child->recompute_position();
  child->recompute_z_index();
  _children.insert(child);

  // This has to be last. Otherwise we're attaching to the VertexPool with outdated positions
  child->set_root(_root);

  return child;
}

INLINE PT(LUIElementIterator) LUIObject::get_children() {
  return new LUIElementIterator(_children.begin(), _children.end());
}

INLINE int LUIObject::get_child_count() {
  return _children.size();
}

INLINE void LUIObject::on_color_changed() {
  LUIBaseElement::on_color_changed();
  
  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_color_changed();
  }
}



INLINE void LUIObject::on_bounds_changed() {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Updating children .. " << endl;
  }

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->recompute_position();
  }
}

INLINE void LUIObject::on_visibility_changed() {
  luiObject_cat.info() << "Todo: On on_visibility_changed" << endl;
}

INLINE void LUIObject::on_z_index_changed() {
  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->recompute_z_index();
  }
}

INLINE void LUIObject::on_detached() {
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

INLINE void LUIObject::remove_child(PT(LUIBaseElement) child) {


  LUIChildVector::iterator child_index = std::find(_children.begin(), _children.end(), child);


  if (child_index == _children.end()) {
    luiObject_cat.warning() << "Attempted to remove child, but child is not attached to this object" << endl;
    return;
  }

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Removing child .." << endl;
  }

  _children.erase(child_index);
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

  // Now clear the vector
  _children.clear();
}


INLINE PT(LUIBaseElement) LUIObject::add_child(PT(LUIBaseElement) child) {

  if (child->get_parent() != NULL) {
    luiObject_cat.error() << "You cannot reattach a child, unattach the child from it's current parent first" << endl;
    return child;
  }

  child->set_parent(this);
  child->recompute_position();
  _children.push_back(child);

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

INLINE void LUIObject::fit_to_children() {

  float maxX = 0;
  float maxY = 0;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    LPoint2 pos = get_relative_pos((*it)->get_abs_pos());
    maxX = max(maxX, pos.get_x() + (*it)->get_width());
    maxY = max(maxY, pos.get_y() + (*it)->get_height());
  }

  set_width(maxX);
  set_height(maxY);

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Fitted to children: " << get_width() << "x" << get_height() << " .." << endl;
  }


}

INLINE void LUIObject::set_sort_children(bool do_sort) {
  _sort_children = do_sort;
}

INLINE bool LUIObject::get_sort_children() {
  return _sort_children;
}
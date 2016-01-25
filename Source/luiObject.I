
INLINE void LUIObject::remove_child(PT(LUIBaseElement) child) {

  if (_content_node != NULL) {
    return _content_node->remove_child(child);
  }

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
  child->set_parent(NULL);

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

  if (_content_node != NULL) {
    return _content_node->add_child(child);
  }


  if (child->get_parent() != NULL) {
    luiObject_cat.error() << "You cannot reattach a child, unattach the child from it's current parent first" << endl;
    return child;
  }

  child->set_parent(this);
  child->recompute_position();
  _children.push_back(child);

  // This has to be last. Otherwise we're attaching to the pool with outdated positions
  child->set_root(_root);

  return child;
}

INLINE PT(LUIElementIterator) LUIObject::get_children() {
  return new LUIElementIterator(_children.begin(), _children.end());
}

INLINE int LUIObject::get_child_count() const {
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
  // _parent = NULL;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->on_detached();
  }

}

INLINE void LUIObject::fit_to_children() {

  float maxX = 0;
  float maxY = 0;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());

    if (child->_placement_x == M_default) {
      maxX = max(maxX, pos.get_x() + child->get_width());
    }

    if (child->_placement_y == M_default) {
      maxY = max(maxY, pos.get_y() + child->get_height());
    }
  }

  maxX = max(get_padding_left(), maxX);
  maxY = max(get_padding_top(), maxY);

  set_size(maxX + get_padding_right(), maxY + get_padding_bottom());
}

INLINE void LUIObject::fit_height_to_children() {
  float maxY = 0;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());
    if (child->_placement_y == M_default) {
      maxY = max(maxY, pos.get_y() + child->get_height());
    }
  }
  maxY = max(get_padding_top(), maxY);
  set_height(maxY + get_padding_bottom());
}


INLINE void LUIObject::fit_width_to_children() {
  float maxX = 0;

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    LUIBaseElement* child = (*it);
    LPoint2 pos = get_relative_pos(child->get_abs_pos());
    if (child->_placement_x == M_default) {
      maxX = max(maxX, pos.get_x() + child->get_width());
    }
  }
  maxX = max(get_padding_left(), maxX);
  set_height(maxX + get_padding_right());
}

INLINE void LUIObject::set_sort_children(bool do_sort) {
  _sort_children = do_sort;
}

INLINE bool LUIObject::get_sort_children() const {
  return _sort_children;
}



INLINE void LUIObject::set_content_node(PT(LUIObject) content_node) {
  _content_node = content_node;
}

INLINE PT(LUIObject) LUIObject::get_content_node() {
  return _content_node;
}

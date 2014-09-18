
/*

INLINE PT(LUISprite) LUIObject::construct_and_attach_sprite(float x, float y, float w, float h) {
  PT(LUISprite) sprite = new LUISprite(this);
  sprite->set_top_left(x, y);
  sprite->set_root(_root);
  sprite->set_parent(this);
  sprite->recompute_z_index();
  _children.insert(sprite);
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source, const string &atlas_id, float x, float y, float w, float h) {

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Attach sprite from atlas descriptor" << endl;
  }

  PT(LUIAtlasDescriptor) descriptor = LUIAtlasPool::get_global_ptr()->get_descriptor(atlas_id, source);

  if (descriptor == NULL) {
    luiObject_cat.error() << "Atlas entry '" << source << "' not found in atlas '" << atlas_id << "'" << endl;
    return NULL;
  }

  PT(LUISprite) sprite = construct_and_attach_sprite(x, y, w, h);
  sprite->set_texture(descriptor);

  // Only set a size if it's valid, otherwise let the sprite auto-detect the size
  if (w > 0.0 && h > 0.0) {
    sprite->set_size(w, h);
  }

  sprite->end_update_section();
  
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source, float x, float y, float w, float h) {

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Attach sprite from string: '" << source << "'" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y, w, h);
  sprite->set_texture(source);

  // Only set a size if it's valid, otherwise let the sprite auto-detect the size
  if (w > 0.0 && h > 0.0) {
    sprite->set_size(w, h);
  }

  sprite->end_update_section();

  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(PT(Texture) tex, float x, float y, float w, float h) {
  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Attach sprite from texture handle" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y, w, h);
  sprite->set_texture(tex);

  // Only set a size if it's valid, otherwise let the sprite auto-detect the size
  if (w > 0.0 && h > 0.0) {
    sprite->set_size(w, h);
  }

  sprite->end_update_section();
  
  return sprite;
}

*/

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

INLINE void LUIObject::refresh_child_positions() {

  if (luiObject_cat.is_spam()) {
    luiObject_cat.spam() << "Updating children .. " << endl;
  }

  for (lui_element_iterator it = _children.begin(); it!= _children.end(); ++it) {
    (*it)->recompute_position();
  }
}

INLINE void LUIObject::refresh_child_visibility() {
  luiObject_cat.error() << "TODO: refresh_child_visibility in LUIObject" << endl;
}

INLINE PT(LUIBaseElement) LUIObject::add_child(PT(LUIBaseElement) child) {
  luiObject_cat.info() << "Addding child .." << endl;

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

INLINE int LUIObject::get_child_count() {
  return _children.size();
}
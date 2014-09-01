

INLINE int LUIObject::get_sprite_count() {
  return _sprites.size();
}


INLINE PT(LUISprite) LUIObject::construct_and_attach_sprite(float x, float y) {
  PT(LUISprite) sprite = new LUISprite(this);
  sprite->set_top_left(x, y);
  sprite->set_root(_root);
  sprite->set_parent(this);
  _sprites.insert(sprite);
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source, const string &atlas_id, float x, float y) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Attach sprite from atlas descriptor" << endl;
  }

  PT(LUIAtlasDescriptor) descriptor = LUIAtlasPool::get_global_ptr()->get_descriptor(atlas_id, source);

  if (descriptor == NULL) {
    lui_cat.error() << "Atlas entry '" << source << "' not found in atlas '" << atlas_id << "'" << endl;
    return NULL;
  }

  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(descriptor);
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source, float x, float y) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Attach sprite from string: '" << source << "'" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(source);
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(PT(Texture) tex, float x, float y) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Attach sprite from texture handle" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(tex);
  return sprite;
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source) {
  return attach_sprite(source, 0, 0);
}

INLINE LUISprite *LUIObject::attach_sprite(const string &source, const string &atlas_id) {
  return attach_sprite(source, atlas_id, 0, 0);
}

INLINE LUISprite *LUIObject::attach_sprite(PT(Texture) tex) {
  return attach_sprite(tex, 0, 0);
}


INLINE void LUIObject::remove_sprite(PT(LUISprite) sprite) {
  if (find(_sprites.begin(), _sprites.end(), sprite) == _sprites.end()) {
    lui_cat.warning() << "Attempted to remove sprite, but sprite is not attached to this node" << endl;
    return;
  }

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Removing sprite .." << endl;
  }

  _sprites.erase(sprite);
  sprite->on_detached();

  if (lui_cat.is_spam()) {
    cout << "Reference count is now: " << sprite->get_ref_count() << endl;
  }
}

INLINE void LUIObject::remove_child(PT(LUIObject) node) {
  if (find(_nodes.begin(), _nodes.end(), node) == _nodes.end()) {
    lui_cat.warning() << "Attempted to remove node, but node is not attached to this node" << endl;
    return;
  }

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Removing node .." << endl;
  }

  _nodes.erase(node);
  node->on_detached();
  
  if (lui_cat.is_spam()) {
    cout << "Reference count is now: " << node->get_ref_count() << endl;
  }
}

INLINE void LUIObject::refresh_child_positions() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Refreshing child positions .. " << endl;
  }

  // Update sprites
  for (lui_sprite_iterator it = _sprites.begin(); it!= _sprites.end(); ++it) {
    (*it)->recompute_position();
  }

  // Updates nodes
  for (lui_object_iterator it = _nodes.begin(); it!= _nodes.end(); ++it) {
    (*it)->recompute_position();
  }
}

INLINE void LUIObject::refresh_child_visibility() {
  // todo
}

INLINE PT(LUIObject) LUIObject::add_child(PT(LUIObject) node) {
  lui_cat.info() << "Addding widget .." << endl;

  if (node->get_parent() != NULL) {
    lui_cat.error() << "You cannot reattach a node, unattach the node from it's current parent first" << endl;
    return node;
  }

  node->set_parent(this);
  node->recompute_position();
  _nodes.insert(node);

  // This has to be last. Otherwise we're attaching to the VertexPool with outdated positions
  lui_cat.spam() << "Setting root on children" << endl;
  node->set_root(_root);

  return node;
}


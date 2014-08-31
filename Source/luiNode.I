

INLINE int LUINode::get_sprite_count() {
  return _sprites.size();
}

INLINE PT(LUISprite) LUINode::get_sprite(int n) {
  if (n < get_sprite_count()) {
    return _sprites[n];
  }

  lui_cat.error() << "Invalid sprite index" << endl;
  return NULL;
}

INLINE LUISprite *LUINode::attach_sprite(const string &source, const string &atlas_id, float x, float y) {

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

INLINE LUISprite *LUINode::attach_sprite(const string &source, float x, float y) {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Attach sprite from string: '" << source << "'" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(source);
  return sprite;
}

INLINE LUISprite *LUINode::attach_sprite(PT(Texture) tex, float x, float y) {
  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Attach sprite from texture handle" << endl;
  }
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(tex);
  return sprite;
}

INLINE LUISprite *LUINode::attach_sprite(const string &source) {
  return attach_sprite(source, 0, 0);
}

INLINE LUISprite *LUINode::attach_sprite(const string &source, const string &atlas_id) {
  return attach_sprite(source, atlas_id, 0, 0);
}

INLINE LUISprite *LUINode::attach_sprite(PT(Texture) tex) {
  return attach_sprite(tex, 0, 0);
}

INLINE PT(LUISprite) LUINode::construct_and_attach_sprite(float x, float y) {
  PT(LUISprite) sprite = new LUISprite(this);
  sprite->set_top_left(x, y);
  sprite->set_root(_root);
  sprite->set_parent(this);
  _sprites.push_back(sprite);
  return sprite;
}

INLINE void LUINode::remove_sprite(PT(LUISprite) sprite) {
  if (find(_sprites.begin(), _sprites.end(), sprite) == _sprites.end()) {
    lui_cat.warning() << "Attempted to remove sprite, but sprite is not attached to this node" << endl;
    return;
  }

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Removing sprite .." << endl;
  }

  _sprites.erase(remove(_sprites.begin(), _sprites.end(),sprite ), _sprites.end());

  sprite->on_detached();

  if (lui_cat.is_spam()) {
    cout << "Reference count is now: " << sprite->get_ref_count() << endl;
  }
}

INLINE void LUINode::remove_child(PT(LUINode) node) {
  if (find(_nodes.begin(), _nodes.end(), node) == _nodes.end()) {
    lui_cat.warning() << "Attempted to remove node, but node is not attached to this node" << endl;
    return;
  }

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Removing node .." << endl;
  }

  _nodes.erase(remove(_nodes.begin(), _nodes.end(),node ), _nodes.end());
  node->on_detached();
  
  if (lui_cat.is_spam()) {
    cout << "Reference count is now: " << node->get_ref_count() << endl;
  }
}

INLINE void LUINode::refresh_child_positions() {

  if (lui_cat.is_spam()) {
    lui_cat.spam() << "Refreshing child positions .. " << endl;
  }

  // Update sprites
  for (int i = 0; i < _sprites.size(); i++) {
    _sprites[i]->recompute_position();
  }  

  // Updates nodes
  for (int i = 0; i < _nodes.size(); i ++) {
    _nodes[i]->recompute_position();
  }

}

INLINE void LUINode::refresh_child_visibility() {
  // todo
}

INLINE PT(LUINode) LUINode::add_child(PT(LUINode) node) {
  lui_cat.info() << "Addding widget .." << endl;

  if (node->get_parent() != NULL) {
    lui_cat.error() << "You cannot reattach a node, unattach the node from it's current parent first" << endl;
    return node;
  }

  node->set_parent(this);
  node->recompute_position();
  _nodes.push_back(node);

  // This has to be last. Otherwise we're attaching to the VertexPool with outdated positions
  lui_cat.spam() << "Setting root on children" << endl;
  node->set_root(_root);

  return node;
}


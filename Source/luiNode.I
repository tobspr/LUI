

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
  lui_cat.spam() << "Attach sprite from atlas descriptor" << endl;

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
  lui_cat.spam() << "Attach sprite from string: '" << source << "'" << endl;
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(source);
  return sprite;
}

INLINE LUISprite *LUINode::attach_sprite(PT(Texture) tex, float x, float y) {
  lui_cat.spam() << "Attach sprite from texture handle" << endl;
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
  _sprites.push_back(sprite);
  return sprite;
}

INLINE void LUINode::remove_sprite(PT(LUISprite) sprite) {
  if (find(_sprites.begin(), _sprites.end(), sprite) == _sprites.end()) {
    lui_cat.warning() << "Attempted to remove sprite, but sprite is not attached to this node" << endl;
    return;
  }

  lui_cat.spam() << "Removing sprite .." << endl;

  _sprites.erase(remove(_sprites.begin(), _sprites.end(),sprite ), _sprites.end());

  cout << "Reference count is now: " << sprite->get_ref_count() << endl;


}

INLINE void LUINode::refresh_sprite_positions() {
  lui_cat.spam() << "Refreshing child positions .. " << endl;
  for (int i = 0; i < _sprites.size(); i++) {
    _sprites[i]->recompute_position();
  }  
}

INLINE void LUINode::refresh_sprite_visibility() {
  // todo
}
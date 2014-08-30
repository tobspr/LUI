

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

INLINE PT(LUISprite) LUINode::attach_sprite(float x, float y, PT(LUIAtlasDescriptor) desc) {
  lui_cat.spam() << "Attach sprite from atlas descriptor" << endl;
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(desc);
  return sprite;
}

INLINE PT(LUISprite) LUINode::attach_sprite(float x, float y, const string &source) {
  lui_cat.spam() << "Attach sprite from string: '" << source << "'" << endl;
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(source);
  return sprite;
}

INLINE PT(LUISprite) LUINode::attach_sprite(float x, float y, PT(Texture) tex) {
  lui_cat.spam() << "Attach sprite from texture handle" << endl;
  PT(LUISprite) sprite = construct_and_attach_sprite(x, y);
  sprite->set_texture(tex);
  return sprite;
}


INLINE PT(LUIAtlasDescriptor) LUINode::get_atlas_image(const string &identifier) {
  return LUIAtlasPool::get_global_ptr()->get_descriptor("default", identifier);
}

INLINE PT(LUIAtlasDescriptor) LUINode::get_atlas_image(const string &atlas_id, const string &identifier) {
  return LUIAtlasPool::get_global_ptr()->get_descriptor(atlas_id, identifier);
}

INLINE PT(LUISprite) LUINode::construct_and_attach_sprite(float x, float y) {
   PT(LUISprite) sprite = new LUISprite(this);
   sprite->set_top_left(x, y);
   _sprites.push_back(sprite);

   // We have to manually increment the reference count, as the sprite is now stored in the vector -
   // Just calling push_back won't increment the reference count. So the object would instantly get deleted,
   // if the app does not keep a reference to it.
   sprite->ref();

   return sprite;
}

INLINE void LUINode::remove_sprite(PT(LUISprite) sprite) {
  if (find(_sprites.begin(), _sprites.end(), sprite) == _sprites.end()) {
    lui_cat.warning() << "Attempted to remove sprite, but sprite is not attached to this node" << endl;
    return;
  }

  lui_cat.spam() << "Removing sprite .." << endl;

  _sprites.erase(remove(_sprites.begin(), _sprites.end(),sprite ), _sprites.end());
   sprite->unref();
}

INLINE const LVector2 &LUINode::get_size() const {
  return _size;
}

INLINE void LUINode::set_size(const LVector2 &size) {
  set_size(size.get_x(), size.get_y());
}

INLINE void LUINode::set_size(float w, float h) {
   _size.set_x(w);
   _size.set_y(h);
   refresh_sprite_positions();
}

INLINE void LUINode::refresh_sprite_positions() {
  for (int i = 0; i < _sprites.size(); i++) {
    _sprites[i]->recompute_position();
  }  
}

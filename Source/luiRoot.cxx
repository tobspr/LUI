
#include "luiRoot.h"


LUIRoot::LUIRoot() {
    lui_cat.info() << "Initialized new LUIRoot\n";
}
LUIRoot::~LUIRoot() {}

LUIVertexPool* LUIRoot::get_vpool_by_texture(Texture* tex) {
  return NULL;
}

void LUIRoot::operator += (PT(LUINode) node) {
  cout << "Add widget (root, forwarding)" << endl;

  // Not sure if this is correct
  *_root += node;
}

PT(LUISprite) LUIRoot::attach_sprite(float x, float y, LUIAtlasDescriptor desc) {
  return _root->attach_sprite(x, y, desc);
}

void LUIRoot::load_atlas(const string &atlas_id, const string &atlas_desc_path, const string &atlas_tex_path) {

  if (_atlases.count(atlas_id) != 0) {
    lui_cat.error() << "Error whilst attaching atlas '" << atlas_id << "'" << endl;
    lui_cat.error() << "You cannot attach multiple atlases with the same name!" << endl;
    return;
  }

  PT(LUIAtlas) atlas = new LUIAtlas();

  if (!atlas->load_descriptor_file(atlas_desc_path)) {
    lui_cat.error() << "Atlas '" << atlas_id << "' failed to load descriptor." << endl;
    return;
  }

  if (!atlas->load_texture(atlas_tex_path)) {
    lui_cat.error() << "Atlas '" << atlas_id << "' failed to load texture." << endl;
    return;
  }

  _atlases[atlas_id] = atlas;

}



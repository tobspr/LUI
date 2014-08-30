
#include "luiAtlasPool.h"


LUIAtlasPool *LUIAtlasPool::_global_ptr = NULL;

LUIAtlasPool::LUIAtlasPool() {
  lui_cat.info() << "Initialized new LUIAtlasPool\n";
}

LUIAtlasPool::~LUIAtlasPool() {
  lui_cat.info() << "Destructed LUIAtlasPool\n";
}

LUIAtlasPool* LUIAtlasPool::get_global_ptr() {
   if (_global_ptr == (LUIAtlasPool *)NULL) {
     _global_ptr = new LUIAtlasPool();
   } 
   return _global_ptr;
}


void LUIAtlasPool::load_atlas(const string &atlas_id, const string &atlas_desc_path, const string &atlas_tex_path) {

  if (_atlases.count(atlas_id) != 0) {
    lui_cat.error() << "Error whilst loading atlas '" << atlas_id << "'" << endl;
    lui_cat.error() << "You cannot load multiple atlases with the same name!" << endl;
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




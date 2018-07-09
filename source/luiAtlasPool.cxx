
#include "luiAtlasPool.h"

LUIAtlasPool* LUIAtlasPool::_global_ptr = nullptr;

/**
 * @brief Constructs the LUIAtlasPool
 * @details This is the private constructor used to construct the global singleton
 */
LUIAtlasPool::LUIAtlasPool() {
}

/**
 * @brief Returns the global LUIAtlasPool instance
 * @details This returns the global instance of the LUIAtlasPool. If no instance
 *   exists yet, it is created first.
 * @return Handle to the global atlas pool instance
 */
LUIAtlasPool* LUIAtlasPool::get_global_ptr() {
  if (_global_ptr == nullptr) {
    _global_ptr = new LUIAtlasPool();
  }
  return _global_ptr;
}

/**
 * @brief Loads an atlas from a given filename and descriptor path
 * @details This loads an atlas with the given name from two files, the descriptor
 *   and texture file. The files should be the ones generated with LUIAtlasGen.
 *
 *   The atlas_desc_path path should point to the file which stores the atlas
 *   entries, in most cases atlas.txt. The atlas_tex_path should point to the
 *   atlas texture file, in most cases atlas.png.
 *
 *   In case the atlas fails to load, an error message is printed and nothing
 *   happens.
 *
 * @param atlas_id Name of the atlas, under which it will be stored
 * @param atlas_desc_path Path to the descriptor file
 * @param atlas_tex_path Path to the atlas texture file
 */
void LUIAtlasPool::load_atlas(const string& atlas_id, const string& atlas_desc_path, const string& atlas_tex_path) {

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

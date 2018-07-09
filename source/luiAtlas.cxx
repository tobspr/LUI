
#include "luiAtlas.h"

#include "samplerState.h"
#include "virtualFileSystem.h"
#include <sstream>


/**
 * @brief Loads a descriptor file
 * @details This loads a descriptor file previously created with LUIAtlasGen.
 *   When the file was loaded, true is returned, otherwise an error is printed
 *   and false is returned.
 *
 * @param descriptor_path Path to the generated atlas file, most times 'atlas.txt'
 * @return true if the atlas file was loaded, false otherwise
 */
bool LUIAtlas::load_descriptor_file(const string& descriptor_path) {

  lui_cat.info() << "Loading atlas description from " << descriptor_path << endl;

  // Get file handle
  VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();
  PT(VirtualFile) file = vfs->get_file(descriptor_path);

  if (file == nullptr) {
    lui_cat.error() << "Could not find " << descriptor_path << endl;
    return false;
  }

  if (!file->is_regular_file()) {
    lui_cat.error() << "File '"<< descriptor_path << "' is not a regular file" << endl;
    return false;
  }

  string content = file->read_file(true);
  stringstream stream(content);

  string name;
  int x, y, w, h;
  while (stream >> name >> x >> y >> w >> h)
  {
    if (has_entry(name))
      lui_cat.warning() << "Entry '" << name << "' is already contained in atlas, overriding .." << endl;
    _entries[name] = LUIAtlasEntry(x, y, w, h);
  }

  return true;
}

/**
 * @brief Loads an atlas texture
 * @details This loads the atlas texture, and prepares it for rendering by setting
 *   several filtering properties on the texture. If the texture was not found,
 *   returns false, otherwise returns true. Also returns false if the texture
 *   has different dimensions in width / height.
 *
 * @param texture_path Path to the atlas texture
 * @return true if the texture was loaded successfully, false otherwise
 */
bool LUIAtlas::load_texture(const string& texture_path) {
  lui_cat.info() << "Loading atlas texture from " << texture_path << endl;

  _tex = TexturePool::load_texture(texture_path);

  // File not found
  if (_tex == nullptr) {
    lui_cat.error() << "Failed to load atlas texture from " << texture_path << endl;
    _tex = nullptr;
    return false;
  }

  // Non square
  if (_tex->get_x_size() != _tex->get_y_size()) {
    lui_cat.error() << "Cannot load non-square atlas texture!" << endl;
    _tex = nullptr;
    return false;
  }

  // Prepare the texture
  _tex->set_minfilter(SamplerState::FT_nearest);
  _tex->set_magfilter(SamplerState::FT_nearest);
  _tex->set_anisotropic_degree(0);
  return true;
}


#include "luiAtlas.h"




LUIAtlas::LUIAtlas() : _size(1) {
  lui_cat.spam() << "Constructed new LUIAtlas" << endl;
}

LUIAtlas::~LUIAtlas() {
   lui_cat.spam() << "Destructed LUIAtlas" << endl;
}



bool LUIAtlas::load_descriptor_file(const string &descriptor_path) {

  lui_cat.info() << "Loading atlas description from " << descriptor_path << endl;


  // This sucks & crashes
  //VirtualFileSystem *vfs = VirtualFileSystem::get_global_ptr();

  //PT(VirtualFile) file = vfs->get_file(descriptor_path);
  //if (file == (VirtualFile *)NULL) {
  //  // No such file.
  //  lui_cat.error()
  //    << "Could not find " << descriptor_path << "\n";
  //  return false;
  //} else {

  //  if (!file->is_regular_file()) {
  //    lui_cat.error() << "File '"<< descriptor_path << "' is not a regular file" << endl;
  //    return false;
  //  }
  //  string content = file->read_file(true);
  //  //cout << "Content is: '" << content << "'";
  //}

  //cout << "Returning .. " << endl;

  // This works perfectly
  // Doesn't support VirtualFileSystem though :(

  std::ifstream infile(descriptor_path);

  string name;
  int x, y, w, h;
  while (infile >> name >> x >> y >> w >> h)
  {
      add_entry(name, x, y, w, h);
  }

  return true;
}

void LUIAtlas::add_entry(const string &name, int x, int y, int w, int h) {

    if(lui_cat.is_spam()) {
      cout << "Registering entry " << name << " at position " << x << " / " << y << " and size " << w << "x" << h << endl;
    }

    LUIAtlasEntry* entry = new LUIAtlasEntry();
    entry->pos = LVector2(x, y);
    entry->size = LVector2(w, h);
    _entries[name] = entry;
}



bool LUIAtlas::load_texture(const string &texture_path) {
    lui_cat.info() << "Loading atlas texture from " << texture_path << endl;

    _tex = TexturePool::load_texture(texture_path);

    if (_tex == NULL) {
      lui_cat.error() << "Failed loading atlas texture" << endl;
      return false;
    }

    _size = _tex->get_x_size();

    return true;
}


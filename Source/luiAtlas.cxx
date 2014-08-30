
#include "luiAtlas.h"



LUIAtlasDescriptor::LUIAtlasDescriptor() {
}

LUIAtlasDescriptor::~LUIAtlasDescriptor() {
}



LUIAtlas::LUIAtlas() : _size(0) {

}


bool LUIAtlas::load_descriptor_file(const string &descriptor_path) {

  lui_cat.info() << "Loading atlas description from " << descriptor_path << endl;


  // This sucks
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

  // This rocks
  std::ifstream infile(descriptor_path);

  string name;
  int x, y, w, h;
  while (infile >> name >> x >> y >> w >> h)
  {
      add_descriptor(name, x, y, w, h);
  }


  return false;
}

void LUIAtlas::add_descriptor(const string &name, int x, int y, int w, int h) {
    cout << "Registering descriptor " << name << " at position " << x << " / " << y << " and size " << w << "x" << h << endl;

}

bool LUIAtlas::load_texture(const string &texture_path) {
    lui_cat.info() << "Loading atlas texture from " << texture_path << endl;

    _tex = TexturePool::load_texture(texture_path);

    if (_tex == NULL) {
      lui_cat.info() << "Failed loading atlas texture" << endl;
      return false;
    }

    return false;
}

LUIAtlas::~LUIAtlas() {

}

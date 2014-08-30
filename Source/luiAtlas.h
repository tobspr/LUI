// Filename: luiAtlas.h
// Created by:  tobspr (29Aug14)
//

#ifndef LUI_ATLAS_H
#define LUI_ATLAS_H

#include <fstream>

#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "texture.h"
#include "virtualFileSystem.h"
#include "texturePool.h"

#include "config_lui.h"


class EXPCL_PANDASKEL LUIAtlasDescriptor : public ReferenceCount {

PUBLISHED:
  LUIAtlasDescriptor();
  ~LUIAtlasDescriptor();

public:

  // Todo: Add getters & setters
  Texture* tex;
  PN_stdfloat width, height;
  LVector2 uv_begin;
  LVector2 uv_end;

  
};




class EXPCL_PANDASKEL LUIAtlas : public ReferenceCount {

public:

  LUIAtlas();
  ~LUIAtlas();

  bool load_descriptor_file(const string &descriptor_path);
  bool load_texture(const string &texture_path);

private:

  void add_descriptor(const string &name, int x, int y, int w, int h);


  PT(Texture) _tex;
  map<string, PT(LUIAtlasDescriptor)> _descriptors;
  int _size;
};



#endif
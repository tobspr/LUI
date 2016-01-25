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

struct LUIAtlasEntry {
  LTexCoord size;
  LTexCoord pos;
};

class EXPCL_LUI LUIAtlas : public ReferenceCount {

PUBLISHED:

  LUIAtlas();
  ~LUIAtlas();

  bool load_descriptor_file(const string &descriptor_path);
  bool load_texture(const string &texture_path);

  INLINE Texture* get_texture() const;

  INLINE bool has_entry(const string &name) const;
  INLINE LUIAtlasEntry* get_entry(const string &name) const;

  INLINE int get_size() const;

private:

  void add_entry(const string &name, int x, int y, int w, int h);

  PT(Texture) _tex;
  pmap<string, LUIAtlasEntry*> _entries;
  int _size;

};

#include "luiAtlas.I"

#endif

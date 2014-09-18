// Filename: luiSprite_ext.h
// Created by:  tobspr (18Sep14)
//

#ifndef LUI_SPRITE_EXT_H
#define LUI_SPRITE_EXT_H

#include "dtoolbase.h"

#ifdef HAVE_PYTHON

#include "extension.h"
#include "luiSprite.h"
#include "py_panda.h"

template<>
class Extension<LUISprite> : public ExtensionBase<LUISprite> {
public:
  virtual int __setattr__(PyObject *self, const string &name, PyObject *value);
};

#endif

#endif

// Filename: luiSprite_ext.cxx
// Created by:  tobspr (18Sep14)
//

#include "luiSprite_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUISprite>::__setattr__(PyObject *self, const string &name, PyObject *value) {
  cout << "Settattr (LUISprite) called" << endl;
  return 0;
}

#endif


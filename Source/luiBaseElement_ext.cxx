// Filename: luiBaseElement_ext.cxx
// Created by:  tobspr (18Sep14)
//

#include "luiBaseElement_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUIBaseElement>::__setattr__(PyObject *self, const string &name, PyObject *value) {
  cout << "Settattr called" << endl;
  return 0;
}

#endif


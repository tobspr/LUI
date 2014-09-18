// Filename: luiBaseElement_ext.cxx
// Created by:  rdb (06Dec11)
//

#include "luiBaseElement_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUIBaseElement>::__setattr__(PyObject *self, const string &name, PyObject *value) {
  cout << "Settattr called" << endl;
  return 0;
}

#endif


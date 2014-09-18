// Filename: luiBaseElement_ext.h
// Created by:  tobspr (18Sep14)
//

#ifndef LUI_BASE_ELEMENT_EXT_H
#define LUI_BASE_ELEMENT_EXT_H

#include "dtoolbase.h"

#ifdef HAVE_PYTHON


#include "extension.h"
#include "luiBaseElement.h"
#include "py_panda.h"

template<>
class Extension<LUIBaseElement> : public ExtensionBase<LUIBaseElement> {
public:
  int __setattr__(PyObject *self, PyObject *name, PyObject *value);
  PyObject *__getattr__(PyObject *self, PyObject *name);
};

#endif
#endif

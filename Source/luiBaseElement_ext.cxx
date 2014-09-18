// Filename: luiBaseElement_ext.cxx
// Created by:  tobspr (18Sep14)
//

#include "luiBaseElement_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUIBaseElement>::__setattr__(PyObject *self, PyObject *name, PyObject *value) {
  cout << "__setattr__ (LUIBaseElement) called for '" << name << "'" << endl;

  PyObject *setter_name = PyString_FromString("set_");
  PyString_Concat(&setter_name, name);

  PyObject *result = PyObject_CallMethodObjArgs(self, setter_name, value, NULL);

  if (result == NULL) {
    Py_DECREF(setter_name);
    return -1;
  }

  Py_DECREF(setter_name);
  Py_DECREF(result);
  return 0;
}

PyObject *Extension<LUIBaseElement>::__getattr__(PyObject *self, PyObject *name) {
  cout << "__getattr__ (LUIBaseElement) called for '" << name << "'" << endl;

  PyObject *getter_name = PyString_FromString("get_");
  PyString_Concat(&getter_name, name);

  PyObject *getter = PyObject_GenericGetAttr(self, getter_name);

  if (getter == NULL) {
    Py_DECREF(getter_name);
    return NULL;
  }

  PyObject *return_value = PyObject_CallObject(getter, NULL);
  Py_DECREF(getter_name);
  // Py_DECREF(getter);
  return return_value;
}

#endif


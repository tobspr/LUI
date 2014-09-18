// Filename: luiBaseElement_ext.cxx
// Created by:  tobspr (18Sep14)
//

#include "luiBaseElement_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUIBaseElement>::__setattr__(PyObject *self, PyObject *name, PyObject *value) {

  // Try to find a method called "set_<name>"
  PyObject *str = PyObject_Str(name);
  string name_as_str;
  if (str != NULL) {
    name_as_str = PyString_AS_STRING(str);
  }
  cout << "__setattr__ (LUIBaseElement) called for '" << name_as_str << "'" << endl;

  if (str != NULL) {
    Py_DECREF(str);
  }

  PyObject *setter_name = PyString_FromString("set_");
  PyString_Concat(&setter_name, name);

  PyObject *result = PyObject_CallMethodObjArgs(self, setter_name, value, NULL);

  // Did not find any method, that means we save the value in the class dict
  if (result == NULL) {
    Py_DECREF(setter_name);

    // Write to class dictionary
    cout << "Could not find element, saving in class dict" << endl; 
    PyObject* __dict__ = PyObject_GenericGetAttr(self, (char *)string("__dict__").c_str()); 
    PyDict_SetItem(__dict__, name, value); 

    Py_DECREF(__dict__);
    return 0;
  }

  Py_DECREF(setter_name);
  Py_DECREF(result);
  return 0;
}

PyObject *Extension<LUIBaseElement>::__getattr__(PyObject *self, PyObject *name) {

  // Try to find a method called "get_<name>"
  PyObject *str = PyObject_Str(name);
  string name_as_str;
  if (str != NULL) {
    name_as_str = PyString_AS_STRING(str);
  }
  cout << "__getattr__ (LUIBaseElement) called for '" << name_as_str << "'" << endl;

  if (str != NULL) {
    Py_DECREF(str);
  }
  PyObject *getter_name = PyString_FromString("get_");
  PyString_Concat(&getter_name, name);

  PyObject *getter = PyObject_GenericGetAttr(self, getter_name);

  // No method found, just return, interrogate will fix this for us
  if (getter == NULL) {
    Py_DECREF(getter_name);
    return NULL;
  }

  // Calls the "get_<name>" and returns the result
  PyObject *return_value = PyObject_CallObject(getter, NULL);
  Py_DECREF(getter_name);
  return return_value;
}

#endif


// Filename: luiBaseElement_ext.cxx
// Created by:  tobspr (18Sep14)
//

#include "luiBaseElement_ext.h"
#include "extension.h"

#ifdef HAVE_PYTHON

int Extension<LUIBaseElement>::__setattr__(PyObject *self, PyObject *name, PyObject *value) {


  PyObject *str = PyObject_Str(name);
  string name_as_str;
  if (str != NULL) {
    name_as_str = PyString_AS_STRING(str);
    Py_DECREF(str);
  }
  // cout << "__setattr__ (LUIBaseElement) called for '" << name_as_str << "'" << endl;

  // Try to find a method called "set_<name>"
  PyObject *setter_name = PyString_FromString("set_");
  PyString_Concat(&setter_name, name);

  // cout << "Check if method exists .." << endl;
  PyObject *setter = PyObject_GenericGetAttr(self, setter_name);
  
  // If such a method exists
  if (setter != NULL) {
    Py_DECREF(setter_name);
    
    // Call the method

    // If the user passed a tuple, we assume the tuple contained the arguments
    if (PyTuple_Check(value)) {
      Py_XDECREF(PyObject_CallObject(setter, value));

    // Otherwise just pass the value
    } else {
      Py_XDECREF(PyObject_CallFunctionObjArgs(setter, value, NULL));
    }

    Py_DECREF(setter);

    // Return success
    return 0;
  }

  Py_DECREF(setter_name);

  // Clear the error stack. This is important, as GenericGetAttr throws an error
  // if the property is not found. And if we don't clear the error stack, interrogate
  // will call getattr (not sure why)
  PyErr_Clear();

  // In this case, no method was found, so return to default implementation
  // cout << "No such attribute/method found, returning to default implementation" << endl;
  return PyObject_GenericSetAttr(self, name, value);

}


PyObject *Extension<LUIBaseElement>::__getattr__(PyObject *self, PyObject *name) {


  PyObject *str = PyObject_Str(name);
  string name_as_str;
  if (str != NULL) {
    name_as_str = PyString_AS_STRING(str);
    Py_DECREF(str);
  }
  // cout << "__getattr__ (LUIBaseElement) called for '" << name_as_str << "'" << endl;

  // Check if there is any attribute / method called <name>
  PyObject *getter = PyObject_GenericGetAttr(self, name);

  if (getter != NULL) {
    // cout << "Direct property found" << endl;
    return getter;
  }

  // Clear the error stack. This is important, as GenericGetAttr throws an error
  // if the property is not found. And if we don't clear the error stack, interrogate
  // will call getattr (not sure why)
  PyErr_Clear();

  // If not, check if there is a method called "get_<name>"
  PyObject *getter_name = PyString_FromString("get_");
  PyString_Concat(&getter_name, name);

  PyObject *get_getter = PyObject_GenericGetAttr(self, getter_name);

  if (get_getter != NULL) {

    // cout << "Attribute function found" << endl;
    Py_DECREF(getter_name);

    PyObject *call_result = PyObject_CallObject(get_getter, NULL);
    Py_DECREF(get_getter);
    return call_result; 

  }

  // Clear the error stack. This is important, as GenericGetAttr throws an error
  // if the property is not found. And if we don't clear the error stack, interrogate
  // will call getattr (not sure why)
  PyErr_Clear();


  Py_DECREF(getter_name);

  // Otherwise there was no property found
  // cout << "Attribute not found. Returning .." << endl;

  // Simulate an attribute error
  Py_XDECREF(PyObject_GenericGetAttr(self, name));


  return NULL;

}

#endif



#include "dtoolbase.h"
#include "interrogate_request.h"

#undef _POSIX_C_SOURCE
#include "py_panda.h"

IMPORT_THIS LibraryDef LUI_moddef;

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef py_LUI_module = {
  PyModuleDef_HEAD_INIT,
  "LUI",
  NULL,
  -1,
  NULL,
  NULL, NULL, NULL, NULL
};

#ifdef _WIN32
extern "C" __declspec(dllexport) PyObject *PyInit_LUI();
#else
extern "C" PyObject *PyInit_LUI();
#endif

PyObject *PyInit_LUI() {
  LibraryDef *defs[] = {&LUI_moddef, NULL};

  return Dtool_PyModuleInitHelper(defs, &py_LUI_module);
}

#else  // Python 2 case

#ifdef _WIN32
extern "C" __declspec(dllexport) void initLUI();
#else
extern "C" void initLUI();
#endif

void initLUI() {
  LibraryDef *defs[] = {&LUI_moddef, NULL};

  Dtool_PyModuleInitHelper(defs, "LUI");
}
#endif


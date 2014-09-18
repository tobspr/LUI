// Filename: luiObject_ext.h
// Created by:  tobspr (18Sep14)
//

#ifndef LUI_OBJECT_EXT_H
#define LUI_OBJECT_EXT_H

#include "dtoolbase.h"

#ifdef HAVE_PYTHON

#include "extension.h"
#include "luiSprite.h"
#include "luiBaseElement_ext.h"
#include "luiObject.h"
#include "py_panda.h"

template<>
class Extension<LUIObject> : public Extension<LUIBaseElement>  {

};

#endif

#endif

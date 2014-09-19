// Filename: luiText_ext.h
// Created by:  tobspr (18Sep14)
//

#ifndef LUI_TEXT_EXT_H
#define LUI_TEXT_EXT_H

#include "dtoolbase.h"

#ifdef HAVE_PYTHON

#include "extension.h"
#include "luiText.h"
#include "luiBaseElement_ext.h"
#include "luiBaseElement.h"
#include "py_panda.h"

template<>
class Extension<LUIText> : public Extension<LUIBaseElement>  {

};

#endif

#endif

// Filename: luiSprite_ext.h
// Created by:  tobspr (18Sep14)
//

#ifndef LUI_SPRITE_EXT_H
#define LUI_SPRITE_EXT_H

#include "dtoolbase.h"

#ifdef HAVE_PYTHON

#include "extension.h"
#include "luiSprite.h"
#include "luiBaseElement_ext.h"
#include "luiBaseElement.h"
#include "py_panda.h"

template<>
class Extension<LUISprite> : public Extension<LUIBaseElement>  {

};

#endif

#endif

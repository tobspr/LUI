// Filename: luiIterators.h
// Created by:  tobspr (01Sep14)
//

#ifndef LUI_ITERATORS_H
#define LUI_ITERATORS_H

#include "pandabase.h"
#include "pandasymbols.h"

class LUIObject;
class LUISprite;


// Iterators
typedef pset<PT(LUIObject)>::iterator lui_object_iterator;
typedef pset<PT(LUISprite)>::iterator lui_sprite_iterator;


#define ITER_CLASS_NAME LUISpriteIterator
#define ITER_VALUE_TYPE LUISprite
#define ITER_ITERATOR_TYPE lui_sprite_iterator

#include "luiIteratorTempl.h"

#undef ITER_CLASS_NAME
#undef ITER_VALLUE_TYPE
#undef ITER_ITERATOR_TYPE


#endif
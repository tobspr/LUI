// Filename: luiIterators.h
// Created by:  tobspr (01Sep14)
//

#ifndef LUI_ITERATORS_H
#define LUI_ITERATORS_H

#include "pandabase.h"
#include "pandasymbols.h"
#include "referenceCount.h"

class LUIBaseElement;

// Iterators
typedef pset<PT(LUIBaseElement)>::iterator lui_element_iterator;

class EXPCL_LUI LUIElementIterator : public ReferenceCount {
PUBLISHED:
  INLINE LUIBaseElement * __next__() {
    if (_iter != _end) {
      return *_iter++;
    }
    return NULL;
  }
  INLINE LUIElementIterator &__iter__() {
    return *this;
  }
public:
  LUIElementIterator(lui_element_iterator begin, lui_element_iterator end) 
    : _iter(begin), _end(end) {
    lui_cat.spam() << "Construct lui iterator" << endl;  
  }
  ~LUIElementIterator() {
    lui_cat.spam() << "Destruct lui iterator " << endl;
  }
private:
  lui_element_iterator _iter;
  lui_element_iterator _end;
};

#endif
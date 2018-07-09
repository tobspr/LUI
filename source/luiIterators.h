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
typedef pvector<PT(LUIBaseElement)>::const_iterator lui_const_element_iterator;

class EXPCL_LUI LUIElementIterator : public ReferenceCount {
PUBLISHED:
  INLINE LUIBaseElement* __next__() {
    if (_iter != _end) {
      return *_iter++;
    }
    return nullptr;
  }
  INLINE LUIElementIterator& __iter__() {
    return *this;
  }
public:
  LUIElementIterator(lui_const_element_iterator begin, lui_const_element_iterator end)
    : _iter(begin), _end(end) {
  }
  ~LUIElementIterator() {
  }
private:
  lui_const_element_iterator _iter;
  lui_const_element_iterator _end;
};

#endif

// Filename: luiIterators.h
// Created by:  tobspr (01Sep14)
//

#ifndef LUI_ITERATORS_H
#define LUI_ITERATORS_H

#include "pandabase.h"
#include "pandasymbols.h"

template <class iterator_type, class object_type>
class EXPCL_PANDASKEL LUIIterator {

PUBLISHED:

  INLINE object_type *__next__() {
    if (_iter != _end) {
      return *_iter++;
    }
    return NULL;
  }

  INLINE LUIIterator &__iter__() {
    return *this;
  }

public:

  // Inline constructor for now
  LUIIterator(const iterator_type &begin, 
    const iterator_type &end) 
    : _iter(begin), _end(end) {
  }

  ~LUIIterator() {
    cout << "Destructed lui iterator " << endl;
  }

protected:
  iterator_type _iter;
  iterator_type _end;
};


#endif
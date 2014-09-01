

class EXPCL_PANDASKEL ITER_CLASS_NAME {

PUBLISHED:

  INLINE ITER_VALUE_TYPE *__next__() {
    if (_iter != _end) {
      return *_iter++;
    }
    return NULL;
  }

  INLINE ITER_CLASS_NAME &__iter__() {
    return *this;
  }

public:

  // Inline constructor for now
  ITER_CLASS_NAME (const ITER_ITERATOR_TYPE &begin, 
    const ITER_ITERATOR_TYPE &end) 
    : _iter(begin), _end(end) {
  }

  ~ ITER_CLASS_NAME () {
    cout << "Destructed lui iterator " << endl;
  }

protected:
  ITER_ITERATOR_TYPE _iter;
  ITER_ITERATOR_TYPE _end;
};

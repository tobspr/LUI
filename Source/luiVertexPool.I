
INLINE int LUIVertexPool::allocate_slot() {

  int next = _slots.get_lowest_off_bit();
  //int next = _last_allocated_slot;
  _last_allocated_slot ++;

  if (lui_cat.is_spam()) {
    cout << "Allocating slot " << next << endl;
  }

  _slots.set_bit(next);
  return next;
}

INLINE void LUIVertexPool::release_slot(int slot) {
  if (lui_cat.is_spam()) {
    cout << "Releasing slot " << slot << endl;
  }
  if (!_slots.get_bit(slot)) {
    lui_cat.error() << "Attempting to release slot but slot is not used " << endl;
    return;
  }
  _slots.set_bit_to(slot, false);
}


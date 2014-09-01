
INLINE int LUIVertexPool::allocate_slot() {

  int next = _slots.get_lowest_off_bit();

  if (lui_cat.is_spam()) {
    cout << "Allocating slot " << next << endl;
  }

  if (next > _highest_index) {
    _highest_index = next;
    if (lui_cat.is_spam()) {
      cout << "Slot " << _highest_index << " is the new highest index" << endl;
    }
  }

  _sprite_count ++;
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

  if (slot > _highest_index) {
    _highest_index = _slots.get_highest_on_bit();
    if (lui_cat.is_spam()) {
      cout << "Slot " << slot << " got detached, highest index is now " << _highest_index << endl;
    }
  }

  _sprite_count --;
  _slots.set_bit_to(slot, false);
}


INLINE void *LUIVertexPool::get_sprite_pointer(int slot) {
  return _vertex_data->modify_array(0)->modify_handle()->get_write_pointer() + sizeof(LUIVertexData) * 4 * slot;
}

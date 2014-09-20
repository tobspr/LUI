


INLINE bool LUIInputHandler::mouse_key_pressed(int index) {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == false && _current_state.mouse_buttons[index] == true;
}

INLINE bool LUIInputHandler::mouse_key_released(int index) {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == true && _current_state.mouse_buttons[index] == false;
}

INLINE string LUIInputHandler::get_key_string(int key) {
  if (_keymap.count(key) == 1) {
    return _keymap[key];
  }
  return "";
}
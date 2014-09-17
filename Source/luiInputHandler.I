


INLINE bool LUIInputHandler::mouse_key_pressed(int index) {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == false && _current_state.mouse_buttons[index] == true;
}

INLINE bool LUIInputHandler::mouse_key_released(int index) {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == true && _current_state.mouse_buttons[index] == false;
}

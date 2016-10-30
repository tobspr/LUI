

INLINE bool LUIInputHandler::mouse_key_pressed(int index) const {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == false && _current_state.mouse_buttons[index] == true;
}

INLINE bool LUIInputHandler::mouse_key_released(int index) const {
  nassertr(index >= 0 && index < 5, false);
  return _last_state.mouse_buttons[index] == true && _current_state.mouse_buttons[index] == false;
}

INLINE string LUIInputHandler::get_key_string(int key) const {
  auto it = _keymap.find(key);
  if (it != _keymap.end()) {
    return it->second;
  }
  return "";
}

INLINE wstring LUIInputHandler::get_mouse_button_name(size_t index) const {
  return wstring(L"mouse-") + std::to_wstring(static_cast<long long>(index));
}

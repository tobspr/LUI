
INLINE string LUIEventData::get_name() const {
  return _event_name;
}

INLINE PT(LUIBaseElement) LUIEventData::get_sender() const {
  return _sender;
}

INLINE LPoint2 LUIEventData::get_coordinates() const {
  return _coordinates;
}

INLINE wstring LUIEventData::get_message() const {
  return _message;
}

INLINE size_t LUIEventData::get_key_modifiers() const {
  return _key_modifiers;
}

INLINE bool LUIEventData::get_modifier_state(KeyModifiers modifier) const {
  return (_key_modifiers & modifier) != 0;
}

INLINE bool LUIEventData::get_modifier_state(const string& modifier_name) const {
  if (modifier_name == "alt") {
    return get_modifier_state(KM_alt);
  } else if (modifier_name == "shift") {
    return get_modifier_state(KM_shift);
  } else if (modifier_name == "ctrl") {
    return get_modifier_state(KM_ctrl);
  }

  lui_cat.error() << "Invalid key modifier name: '" << modifier_name << "'" << endl;
  return false;
}

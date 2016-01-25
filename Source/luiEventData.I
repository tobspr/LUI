
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



INLINE string LUIEventData::get_name() {
  return _event_name;
}


INLINE PT(LUIBaseElement) LUIEventData::get_sender() {
  return _sender;
}

INLINE LPoint2 LUIEventData::get_coordinates() {
  return _coordinates;
}


INLINE string LUIEventData::get_message() {
  return _message;
}


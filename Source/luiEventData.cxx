
#include "luiEventData.h"

TypeHandle LUIEventData::_type_handle;

LUIEventData::LUIEventData(LUIBaseElement* sender, const string& event_name,
                           const wstring& message, const LPoint2& coordinates)
  : CallbackData(),
  _event_name(event_name),
  _sender(sender),
  _coordinates(coordinates),
  _message(message) {
}

LUIEventData::~LUIEventData() {
}

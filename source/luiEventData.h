// Filename: luiEventData.h
// Created by:  tobspr (17Sep14)
//

#ifndef LUI_EVENT_DATA_H
#define LUI_EVENT_DATA_H

#include "config_lui.h"
#include "pandabase.h"
#include "pandasymbols.h"
#include "luse.h"
#include "referenceCount.h"
#include "callbackData.h"
#include "luiBaseElement.h"

class EXPCL_LUI LUIEventData : public CallbackData, public ReferenceCount  {

PUBLISHED:

  // All available key modifiers
  enum KeyModifiers {
    KM_shift = 1,
    KM_alt = 2,
    KM_ctrl = 4
  };


  INLINE string get_name() const;
  INLINE PT(LUIBaseElement) get_sender() const;
  INLINE LPoint2 get_coordinates() const;
  INLINE wstring get_message() const;
  INLINE size_t get_key_modifiers() const;

  // Same as getModifierState in JS
  INLINE bool get_modifier_state(KeyModifiers modifier) const;
  INLINE bool get_modifier_state(const string& modifier_name) const;

  MAKE_PROPERTY(name, get_name);
  MAKE_PROPERTY(sender, get_sender);
  MAKE_PROPERTY(coordinates, get_coordinates);
  MAKE_PROPERTY(message, get_message);
  MAKE_PROPERTY(key_modifiers, get_key_modifiers);

public:

  LUIEventData(LUIBaseElement* sender,
               const string& event_name,
               const wstring& message,
               const LPoint2& coordinates = LPoint2(0),
               size_t key_modifiers = 0);
  ~LUIEventData();

protected:

  string _event_name;
  size_t _key_modifiers;
  wstring _message;
  PT(LUIBaseElement) _sender;
  LPoint2 _coordinates;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    CallbackData::init_type();
    register_type(_type_handle, "LUIEventData", CallbackData::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

};


#include "luiEventData.I"

#endif

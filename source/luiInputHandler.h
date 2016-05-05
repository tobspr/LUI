// Filename: luiInputHandler.h
// Created by:  tobspr (16Sep14)
//

#ifndef LUI_INPUT_HANDLER_H
#define LUI_INPUT_HANDLER_H

#include "config_lui.h"
#include "dataNode.h"
#include "buttonHandle.h"
#include "luiRoot.h"
#include "luiBaseElement.h"

class LUIBaseElement;

class EXPCL_LUI LUIInputHandler : public DataNode {

PUBLISHED:

  LUIInputHandler(const string& name = string());
  virtual ~LUIInputHandler();

public:

  // Inherited from DataNode
  virtual void do_transmit_data(DataGraphTraverser* trav,
                                const DataNodeTransmit& input,
                                DataNodeTransmit& output);
  void process(LUIRoot* root);

protected:

  struct LUIInputState {
    LVecBase2 mouse_pos;
    bool has_mouse_pos;
    bool mouse_buttons[5];
    size_t key_modifiers;
  };

  enum LUIKeyEventMode {
    M_up,
    M_down,
    M_repeat,
    M_press
  };

  struct LUIKeyEvent {
    string btn_name;
    LUIKeyEventMode mode;
  };

  INLINE string get_key_string(int key) const;
  INLINE wstring get_mouse_button_name(size_t index) const;

  void trigger_event(LUIBaseElement* sender, const string& name,
                     const wstring& message = L"") const;

  LUIBaseElement* _hover_element;
  vector<LUIBaseElement*> _mouse_down_elements;
  LUIBaseElement* _focused_element;

  int _mouse_pos_input;
  int _buttons_input;

  INLINE bool mouse_key_pressed(int index) const;
  INLINE bool mouse_key_released(int index) const;

  LUIInputState _last_state;
  LUIInputState _current_state;

  pmap<int, string> _keymap;
  vector<LUIKeyEvent> _key_events;
  vector<int> _text_events;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DataNode::init_type();
    register_type(_type_handle, "LUIInputHandler",
                  DataNode::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

};

#include "luiInputHandler.I"

#endif

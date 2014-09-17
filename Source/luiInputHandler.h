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

class EXPCL_LUI LUIInputHandler : public DataNode {

PUBLISHED:

  LUIInputHandler(const string &name = string());
  virtual ~LUIInputHandler();

public:

  // Inherited from DataNode
  virtual void do_transmit_data(DataGraphTraverser *trav,
                                const DataNodeTransmit &input,
                                DataNodeTransmit &output);
  void process(LUIRoot *root); 

protected:

  struct LUIInputState {
    LVecBase2 mouse_pos;
    bool has_mouse_pos;
    bool mouse_buttons[5];
  };

  LUIBaseElement *_hover_element;
  
  int _mouse_pos_input;
  int _buttons_input;

  LUIInputState _last_state;
  LUIInputState _current_state;

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
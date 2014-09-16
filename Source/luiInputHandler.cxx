
#include "luiInputHandler.h"
#include "buttonEventList.h"
#include "dataGraphTraverser.h"
#include "linmath_events.h"
#include "keyboardButton.h"
#include "mouseButton.h"

TypeHandle LUIInputHandler::_type_handle;

LUIInputHandler::LUIInputHandler(const string &name) : DataNode(name) {
  _mouse_pos_input =  define_input("pixel_xy", EventStoreVec2::get_class_type());
}

LUIInputHandler::~LUIInputHandler() {

}

// Inherited from DataNode
void LUIInputHandler::do_transmit_data(DataGraphTraverser *trav,
                              const DataNodeTransmit &input,
                              DataNodeTransmit &output) {


  _has_mouse = false;

  if (input.has_data(_mouse_pos_input)) {
    // The mouse is within the window.  Get the current mouse position.
    const EventStoreVec2 *mouse_pos;
    DCAST_INTO_V(mouse_pos, input.get_data(_mouse_pos_input).get_ptr());
    _mouse_pos = mouse_pos->get_value();
    _has_mouse = true;
  }
  
}

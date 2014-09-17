
#include "luiInputHandler.h"
#include "buttonEventList.h"
#include "dataGraphTraverser.h"
#include "linmath_events.h"
#include "keyboardButton.h"
#include "mouseButton.h"

TypeHandle LUIInputHandler::_type_handle;

LUIInputHandler::LUIInputHandler(const string &name) : 
  DataNode(name) {
  _mouse_pos_input =  define_input("pixel_xy", EventStoreVec2::get_class_type());
  _buttons_input = define_input("button_events", ButtonEventList::get_class_type());
}

LUIInputHandler::~LUIInputHandler() {

}

// Inherited from DataNode
void LUIInputHandler::do_transmit_data(DataGraphTraverser *trav,
                              const DataNodeTransmit &input,
                              DataNodeTransmit &output) {

  if (input.has_data(_mouse_pos_input)) {
    // The mouse is within the window.  Get the current mouse position.
    const EventStoreVec2 *mouse_pos;
    DCAST_INTO_V(mouse_pos, input.get_data(_mouse_pos_input).get_ptr());
    
    _current_state.mouse_pos = mouse_pos->get_value();
    _current_state.has_mouse_pos = true;
  } else {
    _current_state.has_mouse_pos = false;
    _current_state.mouse_pos = LPoint2(0);
  }
  

  if (input.has_data(_buttons_input)) {
    const ButtonEventList *this_button_events;
    DCAST_INTO_V(this_button_events, input.get_data(_buttons_input).get_ptr());
    int num_events = this_button_events->get_num_events();

    for (int i = 0; i < num_events; i++) {
      const ButtonEvent &be = this_button_events->get_event(i);

      // Button Down
      if (be._type == ButtonEvent::T_down) {
        // if (be._button == KeyboardButton::control()) {
        //   _modifiers |= KM_CTRL;
        // } else if (be._button == KeyboardButton::shift()) {
        //   _modifiers |= KM_SHIFT;
        // } else if (be._button == KeyboardButton::alt()) {
        //   _modifiers |= KM_ALT;
        // } else if (be._button == KeyboardButton::meta()) {
        //   _modifiers |= KM_META;

        // } else if (be._button == KeyboardButton::enter()) {
        //   _text_input.push_back('\n');

        // } else if (be._button == MouseButton::wheel_up()) {
        //   _wheel_delta -= 1;
        // } else if (be._button == MouseButton::wheel_down()) {
        //   _wheel_delta += 1;

        if (be._button == MouseButton::one()) {
          _current_state.mouse_buttons[0] = true;
        } else if (be._button == MouseButton::two()) {
          _current_state.mouse_buttons[1] = true;
        } else if (be._button == MouseButton::three()) {
          _current_state.mouse_buttons[2] = true;
        } else if (be._button == MouseButton::four()) {
          _current_state.mouse_buttons[3] = true;
        } else if (be._button == MouseButton::five()) {
          _current_state.mouse_buttons[4] = true;
        }

      } else if (be._type == ButtonEvent::T_up) {

        if (be._button == MouseButton::one()) {
          _current_state.mouse_buttons[0] = false;
        } else if (be._button == MouseButton::two()) {
          _current_state.mouse_buttons[1] = false;
        } else if (be._button == MouseButton::three()) {
          _current_state.mouse_buttons[2] = false;
        } else if (be._button == MouseButton::four()) {
          _current_state.mouse_buttons[3] = false;
        } else if (be._button == MouseButton::five()) {
          _current_state.mouse_buttons[4] = false;
        }


      }
    }
  }
}

void LUIInputHandler::process(LUIRoot *root) {

  LUIBaseElement *current_hover = NULL;
  float current_hover_z_index = -1000000.0;

  if (_current_state.has_mouse_pos) {
    
      // Iterate all event objects, and find the one with the highest z-index
      // below the cursor
      LUIEventObjectSet::iterator iter = root->get_event_objects_begin();
      LUIEventObjectSet::iterator end = root->get_event_objects_end();
      for (;iter != end; ++iter) {
        LUIBaseElement *elem = *iter;
        if (elem->get_absolute_z_index() > current_hover_z_index &&
            elem->intersects(
              _current_state.mouse_pos.get_x(), 
              _current_state.mouse_pos.get_y())) {
          current_hover = elem;
          current_hover_z_index = elem->get_absolute_z_index();
      }
    }
  }



  // Check for mouse over / out events
  if (current_hover != _hover_element) {
    if (_hover_element != NULL) {
      _hover_element->trigger_event("mouseout", "", _current_state.mouse_pos);
    }

    if (current_hover != NULL) {
      current_hover->trigger_event("mouseover", "", _current_state.mouse_pos);
    }
    _hover_element = current_hover;
  }

  // Check for click events

  // if (_last_state.mouse_buttons[0] == false && _current_state.mouse_buttons[0] == true) {
  //   cout << "Mouse down (0)!!" << endl;
  // }

  // if (_last_state.mouse_buttons[1] == false && _current_state.mouse_buttons[1] == true) {
  //   cout << "Mouse down (1)!!" << endl;
  // }


  if (_last_state.mouse_buttons[2] == false && _current_state.mouse_buttons[2] == true) {
    cout << "Mouse down (2)!" << endl;
  }
  if (_last_state.mouse_buttons[2] == true && _current_state.mouse_buttons[2] == false) {
    cout << "Mouse up (2)!" << endl;
  }



  _last_state = _current_state;

}

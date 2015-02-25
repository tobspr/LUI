
#include "luiInputHandler.h"
#include "buttonEventList.h"
#include "dataGraphTraverser.h"
#include "linmath_events.h"
#include "keyboardButton.h"
#include "mouseButton.h"

TypeHandle LUIInputHandler::_type_handle;

LUIInputHandler::LUIInputHandler(const string &name) :
  DataNode(name),
  _hover_element(NULL),
  _mouse_down_element(NULL),
  _focused_element(NULL)
{
  // Work around crazy issue with MouseWatcher input type not matching up
  ParamVecBase2f::init_type("ParamVecBase2f");

  _mouse_pos_input = define_input("pixel_xy", ParamVecBase2f::get_class_type());
  _buttons_input = define_input("button_events", ButtonEventList::get_class_type());

  // Init states
  for (int i = 0; i < 5; i++) {
    _current_state.mouse_buttons[0] = 0;
    _last_state.mouse_buttons[0] = 0;
  }

  _current_state.has_mouse_pos = false;
  _last_state.has_mouse_pos = false;

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
  

  _key_events.clear();
  _text_events.clear();

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
        } else {
          LUIKeyEvent event = {be._button.get_name(), M_down};
          _key_events.push_back(event);
        }

      } else if (be._type == ButtonEvent::T_repeat) {
        
        LUIKeyEvent event = {be._button.get_name(), M_repeat};
        _key_events.push_back(event);

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
        } else {

        LUIKeyEvent event = {be._button.get_name(), M_up};
        _key_events.push_back(event);
        }

      } else if (be._type == ButtonEvent::T_keystroke) {

        // Ignore control characters; otherwise, they actually get added to strings in the UI.
        if (be._keycode > 0x1F && (be._keycode < 0x7F || be._keycode > 0x9F)) {
          _text_events.push_back(be._keycode);
        }

      }
    }
  }
}

void LUIInputHandler::process(LUIRoot *root) {

  LUIBaseElement *current_hover = NULL;
  int current_render_index = -1;

  if (_current_state.has_mouse_pos) {
    
      // Iterate all event objects, and find the one with the highest z-index
      // below the cursor
      LUIEventObjectSet::iterator iter = root->get_event_objects_begin();
      LUIEventObjectSet::iterator end = root->get_event_objects_end();
      for (;iter != end; ++iter) {
        LUIBaseElement *elem = *iter;
        if (
            // Visible
            elem->get_last_frame_visible() >= root->get_frame_index() && 
            // In front of the last element
            elem->get_last_render_index() > current_render_index &&
            // Under the mouse cursor
            elem->intersects(
              _current_state.mouse_pos.get_x(), 
              _current_state.mouse_pos.get_y())) {
          current_hover = elem;
          current_render_index = elem->get_last_render_index();     
      }
    }
  }

  // Check for mouse over / out events
  if (current_hover != _hover_element) {
    if (_hover_element != NULL) {
      _hover_element->trigger_event("mouseout", wstring(), _current_state.mouse_pos);
    }

    if (current_hover != NULL) {
      current_hover->trigger_event("mouseover", wstring(), _current_state.mouse_pos);
    }
    _hover_element = current_hover;
  }

  // Check for mouse move
  // --- Currently disabled, it's spamming the console ---
  // ^ it's enabled
  if (true) {
    if (_current_state.mouse_pos != _last_state.mouse_pos) {
      // Send a event to the hovered element
      if (_hover_element != NULL) {
        _hover_element->trigger_event("mousemove", wstring(), _current_state.mouse_pos);
      }

      // The focus element also recieves a mousemove element
      if (_focused_element != NULL) {
        _focused_element->trigger_event("mousemove", wstring(), _current_state.mouse_pos);
      }
    }
  }

  // Check for click events
  int click_mouse_button = 0;

  if (mouse_key_pressed(click_mouse_button)) {
    if (_hover_element != NULL) {
      _mouse_down_element = _hover_element;
      _hover_element->trigger_event("mousedown", wstring(), _current_state.mouse_pos);
    }

  }
  if (mouse_key_released(click_mouse_button)) {
    if (_mouse_down_element != NULL) {
      _mouse_down_element->trigger_event("mouseup", wstring(), _current_state.mouse_pos);
    }

    if (_mouse_down_element != NULL && _mouse_down_element == _hover_element) {
      _mouse_down_element->trigger_event("click", wstring(), _current_state.mouse_pos);
    }
  }

  // Manage focus requests
  LUIBaseElement *requested_focus = root->get_requested_focus();

  if (requested_focus == NULL) {

    if (_focused_element != NULL) {
      _focused_element->set_focus(false);
      _focused_element->trigger_event("blur", wstring(), _current_state.mouse_pos);
      _focused_element = NULL;
    }

  } else {

    if (requested_focus != _focused_element) {
      if (lui_cat.is_spam()) {
        lui_cat.spam() << "Focus changed to " 
          << requested_focus 
          << " from " << _focused_element << endl;
      }
      requested_focus->set_focus(true);
      requested_focus->trigger_event("focus" , wstring(), _current_state.mouse_pos);

      if (_focused_element != NULL) {
        _focused_element->set_focus(false);
        _focused_element->trigger_event("blur", wstring(), _current_state.mouse_pos);
      }

      _focused_element = requested_focus;
    }
  }



  // Check key events
  if (_focused_element != NULL) {
    vector<LUIKeyEvent>::const_iterator it;
    for (it = _key_events.begin(); it != _key_events.end(); ++it) {

      string btn_name((*it).btn_name);
      wstring btn_name_w(btn_name.begin(), btn_name.end());

      switch ((*it).mode) {
      case M_down:
        _focused_element->trigger_event("keydown", btn_name_w, _current_state.mouse_pos);
        break;

      case M_up:
        _focused_element->trigger_event("keyup", btn_name_w, _current_state.mouse_pos);
        break;

      case M_repeat:
        _focused_element->trigger_event("keyrepeat", btn_name_w, _current_state.mouse_pos);
        break;

      case M_press:
        break;
      }
    }

    for (vector<int>::iterator it = _text_events.begin(); it != _text_events.end(); ++it) {
      _focused_element->trigger_event("textinput", wstring(1, (unsigned short)(*it)), _current_state.mouse_pos);
    }


    // Focus tick
    _focused_element->trigger_event("tick", wstring(), _current_state.mouse_pos);

  }

  _last_state = _current_state;
}

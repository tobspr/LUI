
#include "luiInputHandler.h"
#include "luiEventData.h"
#include "buttonEventList.h"
#include "dataGraphTraverser.h"
#include "linmath_events.h"
#include "keyboardButton.h"
#include "mouseButton.h"

TypeHandle LUIInputHandler::_type_handle;

LUIInputHandler::LUIInputHandler(const string& name) :
  DataNode(name),
  _hover_element(nullptr),
  _focused_element(nullptr)
{
  _mouse_down_elements.resize(5, nullptr);
  _mouse_pos_input = define_input("pixel_xy", EventStoreVec2::get_class_type());
  _buttons_input = define_input("button_events", ButtonEventList::get_class_type());

  for (int i = 0; i < 5; i++) {
    _current_state.mouse_buttons[i] = false;
  }
  _current_state.mouse_pos.set(-1, -1);
  _current_state.has_mouse_pos = false;
  _current_state.key_modifiers = 0;

  _last_state = _current_state;

}

LUIInputHandler::~LUIInputHandler() {

}

// Inherited from DataNode
void LUIInputHandler::do_transmit_data(DataGraphTraverser* trav,
                              const DataNodeTransmit& input,
                              DataNodeTransmit& output) {

  if (input.has_data(_mouse_pos_input)) {
    // The mouse is within the window.  Get the current mouse position.
    const EventStoreVec2* mouse_pos;
    DCAST_INTO_V(mouse_pos, input.get_data(_mouse_pos_input).get_ptr());

    _current_state.has_mouse_pos = true;
    _current_state.mouse_pos = mouse_pos->get_value();
  } else {
    _current_state.has_mouse_pos = false;
    _current_state.mouse_pos = LPoint2(0);
  }

  _key_events.clear();
  _text_events.clear();

  if (input.has_data(_buttons_input)) {
    const ButtonEventList* this_button_events;
    DCAST_INTO_V(this_button_events, input.get_data(_buttons_input).get_ptr());
    int num_events = this_button_events->get_num_events();

    for (int i = 0; i < num_events; ++i) {
      const ButtonEvent& be = this_button_events->get_event(i);

      // Button Down
      if (be._type == ButtonEvent::T_down) {
        if (be._button == KeyboardButton::control()) {
          _current_state.key_modifiers |= LUIEventData::KM_ctrl;
        } else if (be._button == KeyboardButton::shift()) {
          _current_state.key_modifiers |= LUIEventData::KM_shift;
        } else if (be._button == KeyboardButton::alt()) {
          _current_state.key_modifiers |= LUIEventData::KM_alt;
        }

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

        if (be._button == KeyboardButton::control()) {
          _current_state.key_modifiers &= ~LUIEventData::KM_ctrl;
        } else if (be._button == KeyboardButton::shift()) {
          _current_state.key_modifiers &= ~LUIEventData::KM_shift;
        } else if (be._button == KeyboardButton::alt()) {
          _current_state.key_modifiers &= ~LUIEventData::KM_alt;
        }

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

        // Ignore control characters; otherwise they actually get added to strings in the UI.
        if (be._keycode > 0x1F && (be._keycode < 0x7F || be._keycode > 0x9F)) {
          _text_events.push_back(be._keycode);
        }

      }
    }
  }
}

void LUIInputHandler::process(LUIRoot* root) {
  LUIBaseElement* current_hover = nullptr;
  int current_render_index = -1;

  if (_current_state.has_mouse_pos) {

      // Iterate all event objects, and find the one with the highest z-index
      // below the cursor
      LUIEventObjectSet::iterator iter = root->get_event_objects_begin();
      LUIEventObjectSet::iterator end = root->get_event_objects_end();
      for (;iter != end; ++iter) {
        LUIBaseElement* elem = *iter;
        if (
            // Visible
            elem->get_last_frame_visible() >= root->get_frame_index() &&
            // In front of the last element
            elem->get_last_render_index() > current_render_index &&
            // Under the mouse cursor
            elem->intersects(
              _current_state.mouse_pos.get_x(),
              _current_state.mouse_pos.get_y()) &&
            // Visible #2
            elem->is_visible()) {
          current_hover = elem;
          current_render_index = elem->get_last_render_index();
      }
    }
  }

  // Check for mouse over / out events
  if (current_hover != _hover_element) {
    if (_hover_element != nullptr) {

      trigger_event(_hover_element, "mouseout");
    }

    if (current_hover != nullptr) {
      trigger_event(current_hover, "mouseover");
    }
    _hover_element = current_hover;
  }

  // Check for mouse move
  if (_current_state.mouse_pos != _last_state.mouse_pos) {
    // Send a event to the hovered element
    if (_hover_element != nullptr) {
      trigger_event(_hover_element, "mousemove");
    }

    // The focus element also recieves a mousemove element
    if (_focused_element != nullptr) {
      trigger_event(_focused_element, "mousemove");
    }
  }

  // Check for click events
  // int click_mouse_button = 0;
  bool lost_focus = false;
  for (size_t mouse_button = 0; mouse_button < 5; ++mouse_button) {

    if (mouse_key_pressed(mouse_button)) {
      if (_hover_element != nullptr && _hover_element->is_visible()) {
        _mouse_down_elements[mouse_button] = _hover_element;

        trigger_event(_hover_element, "mousedown", get_mouse_button_name(mouse_button));

        if (_focused_element != nullptr && _hover_element != _focused_element) {
          // When clicking somewhere, and the clicked element is not the focused one,
          // make the focused one loose focus
          lost_focus = true;
        }
      }
    }

    if (mouse_key_released(mouse_button)) {
      if (_mouse_down_elements[mouse_button] != nullptr) {
        trigger_event(_mouse_down_elements[mouse_button], "mouseup", get_mouse_button_name(mouse_button));
      }

      if (_mouse_down_elements[mouse_button] != nullptr && _mouse_down_elements[mouse_button] == _hover_element) {
        trigger_event(_mouse_down_elements[mouse_button], "click", get_mouse_button_name(mouse_button));
      }
    }
  }

  // Manage focus requests
  LUIBaseElement* requested_focus = root->get_requested_focus();


  if (requested_focus == nullptr) {
    // No focus request, eveything remains the same
    // However, when the user clicked somewhere, and it was not the focused element,
    // make it loose the focus. It is important this happens after calling the
    // click event, otherwise we might loose events.

    if (_focused_element != nullptr && (lost_focus || root->get_explicit_blur())) {
      _focused_element->set_focus(false);
      trigger_event(_focused_element, "blur");
      _focused_element = nullptr;
    }
  } else {
    // Focus was requested, and its different from the current focused element
    if (requested_focus != _focused_element) {

      // Tell the currently focused element its no longer focused
      if (_focused_element != nullptr) {
        _focused_element->set_focus(false);
        trigger_event(_focused_element, "blur");
        _focused_element = nullptr;
      }

      // Tell the new element its now focused
      requested_focus->set_focus(true);
      trigger_event(requested_focus, "focus");

      _focused_element = requested_focus;
    }
  }


  // Reset any requested focus, since the element should be in focus now 
  if (root->get_requested_focus()) {
    root->set_requested_focus(nullptr);
  }
  
  root->clear_explicit_blur();

  // Check key events
  if (_focused_element != nullptr && _focused_element->is_visible()) {
    vector<LUIKeyEvent>::const_iterator it;
    for (it = _key_events.begin(); it != _key_events.end(); ++it) {

      string btn_name((*it).btn_name);
      wstring btn_name_w(btn_name.begin(), btn_name.end());

      switch ((*it).mode) {
      case M_down:
        trigger_event(_focused_element, "keydown", btn_name_w);
        break;

      case M_up:
        trigger_event(_focused_element, "keyup", btn_name_w);
        break;

      case M_repeat:
        trigger_event(_focused_element, "keyrepeat", btn_name_w);
        break;

      case M_press:
        break;
      }
    }

    for (vector<int>::iterator it = _text_events.begin(); it != _text_events.end(); ++it) {
      trigger_event(_focused_element, "textinput", wstring(1, (unsigned short)(*it)));
    }

    // Focus tick, only on the focus element to save performance
    trigger_event(_focused_element, "tick");
  }

  _last_state = _current_state;
}

INLINE void LUIInputHandler::trigger_event(LUIBaseElement* sender,
    const string& name, const wstring& message) const {
  sender->trigger_event(
    new LUIEventData(sender, name, message, _current_state.mouse_pos, _current_state.key_modifiers));
}


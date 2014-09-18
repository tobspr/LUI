


#include "luiBaseElement.h"
#include "luiRoot.h"

TypeHandle LUIBaseElement::_type_handle;


NotifyCategoryDef(luiBaseElement, ":lui");

LUIBaseElement::LUIBaseElement() :   
  _visible(true), 
  _offset_x(0),
  _offset_y(0),
  _pos_x(0),
  _pos_y(0),
  _placement_x(M_default),
  _placement_y(M_default),
  _size(0),
  _parent(NULL),
  _root(NULL),
  _local_z_index(0.5),
  _z_index(0.0),
  _events_registered(false),
  _in_update_section(false),
  _snap_position(true)
{

  // We could do _margin() but that gives a warning
  for (int i = 0; i < 4; ++i) {
    _margin[i] = 0.0;
  }
}

LUIBaseElement::~LUIBaseElement() {
  _events.clear();
}

void LUIBaseElement::recompute_position() {
  if (_in_update_section) return;

  // Recompute actual position from top/bottom and left/right offsets
  LVector2 parent_size(0);
  LVector2 parent_pos(0);

  if (_parent != (LUIBaseElement*)NULL) {
    parent_size = _parent->get_size();
    parent_pos = _parent->get_abs_pos();
  };

  if (luiBaseElement_cat.is_spam()) {
    luiBaseElement_cat.spam() << "Recomputing, bounds = " << parent_size.get_x() << ", " 
      << parent_size.get_y() << ", pos = " << parent_pos.get_x() 
      << ", " << parent_pos.get_y() << endl;
  }

  // Vertical Placement

  // Stick top
  if (_placement_y == M_default) {
    _pos_y = _offset_y + get_margin_top();

  // Stick bottom
  } else if (_placement_y == M_inverse) {
    _pos_y = parent_size.get_y() - _offset_y - _size.get_y() - get_margin_bottom();

  // Center Element
  } else {
    _pos_y = (parent_size.get_y() - _size.get_y()) / 2.0 + (get_margin_top() - get_margin_bottom());
  }

  // Horizontal placement

  // Stick left
  if (_placement_x == M_default) {
    _pos_x = _offset_x + get_margin_left();

  // Stick right
  } else if (_placement_x == M_inverse) {
    _pos_x = parent_size.get_x() - _offset_x - _size.get_x() - get_margin_right();
  
  // Center Element
  } else {
    _pos_x = (parent_size.get_x() - _size.get_x()) / 2.0 + (get_margin_left() - get_margin_right());
  }

  _pos_x += parent_pos.get_x();
  _pos_y += parent_pos.get_y();

  if (_snap_position) {
    _pos_x = ceil(_pos_x);
    _pos_y = ceil(_pos_y);
  }

  on_bounds_changed();
}

void LUIBaseElement::register_events() {

  if (_root != NULL && _parent != NULL && !_events_registered && _events.size() > 0) {
      _root->register_event_object(this);
      _events_registered = true;

      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Registering events for object .." << endl;
      }
  } else {
    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Did not register events, root = " << (_root==NULL?"NULL":"valid") << ", registered = " << (_events_registered ? "1":"0") << ", parent = " << (_parent==NULL?"NULL" : "valid") << " .." << endl;
    }
  }
}

void LUIBaseElement::unregister_events() {

  if (_root != NULL && _events_registered) {
    _root->unregister_event_object(this);
    _events_registered = false;
  
    if (luiBaseElement_cat.is_spam()) {
      luiBaseElement_cat.spam() << "Un-registering events for object .." << endl;
    }
  } else {
      if (luiBaseElement_cat.is_spam()) {
        luiBaseElement_cat.spam() << "Did not unregister events, root = " << (_root==NULL?"NULL":"valid") << ", registered = " << (_events_registered ? "1":"0") << " .." << endl;
      }
  }
}

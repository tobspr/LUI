


#include "luiBaseElement.h"

TypeHandle LUIBaseElement::_type_handle;


NotifyCategoryDef(luiBaseElement, ":lui");

LUIBaseElement::LUIBaseElement() :   
  _visible(true), 
  _offset_x(0),
  _offset_y(0),
  _pos_x(0),
  _pos_y(0),
  _stick_top(true),
  _stick_left(true),
  _size(0),
  _parent(NULL),
  _root(NULL),
  _local_z_index(0.5),
  _z_index(0.0),
  _events_registered(false),
  _in_update_section(false)
{
}

LUIBaseElement::~LUIBaseElement() {
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

  if (_stick_top) {
    _pos_y = _offset_y;
  } else {
    _pos_y = parent_size.get_y() - _offset_y - _size.get_y();
  }

  if (_stick_left) {
    _pos_x = _offset_x;
  } else {
    _pos_x = parent_size.get_x() - _offset_x - _size.get_x();
  }

  _pos_x += parent_pos.get_x();
  _pos_y += parent_pos.get_y();

  on_bounds_changed();
}


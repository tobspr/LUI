


INLINE void LUIBaseElement::set_top_left(float x, float y) {
  if (lui_cat.is_spam()) {
    cout << "Set Pos: " << x << "/" << y << endl;
  }
  _stick_top = true;
  _stick_left = true;
  _offset_x = x;
  _offset_y = y;
  recompute_position();
  
}

INLINE void LUIBaseElement::set_top(float top) {
  _stick_top = true;
  _offset_y = top;
  recompute_position();
}

INLINE void LUIBaseElement::set_bottom(float bottom) {
  _stick_top = false;
  _offset_y = bottom;
  recompute_position();
}

INLINE void LUIBaseElement::set_left(float left) {
  _stick_left = true;
  _offset_x = left;
  recompute_position();
}

INLINE void LUIBaseElement::set_right(float right) {
  _stick_left = false;
  _offset_x = right;
  recompute_position();
}
		
INLINE void LUIBaseElement::set_visible(bool visible) {
  _visible = visible;
  on_visibility_changed();
}

INLINE bool LUIBaseElement::is_visible() {
  return _visible;
}

INLINE void LUIBaseElement::hide() {
  set_visible(false);
}

INLINE void LUIBaseElement::show() {
  set_visible(true);
}

INLINE void LUIBaseElement::set_size(const LVector2 &size) {
  set_size(size.get_x(), size.get_y());
}

INLINE void LUIBaseElement::set_size(float w, float h) {
  _size.set_x(w);
  _size.set_y(h);
  on_size_changed();
  recompute_position();
}

INLINE void LUIBaseElement::set_width(float w) {
  _size.set_x(w);
  on_size_changed();
  recompute_position();
}

INLINE void LUIBaseElement::set_height(float h) {
  _size.set_y(h);
  on_size_changed();
  recompute_position();
}

INLINE const LVector2 &LUIBaseElement::get_size() const {
    return _size;
}

INLINE void LUIBaseElement::recompute_position() {
  // Recompute actual position from top/bottom and left/right offsets
  LVector2 parent_size(0);
  
  if (_parent != NULL) {
    parent_size = _parent->get_size();
  };

  if (lui_cat.is_spam() && lui_cat.is_spam()) {
    cout << "Recomputing position, parent size is " << parent_size.get_x() << "x" << parent_size.get_y() << endl;
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

  on_position_changed();
}

INLINE void LUIBaseElement::set_parent(LUIBaseElement* parent) {
  _parent = parent;
}

INLINE LUIBaseElement* LUIBaseElement::get_parent() {
  return _parent;
}
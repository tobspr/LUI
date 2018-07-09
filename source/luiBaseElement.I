

/**
 * @brief Binds a new event handler for a given event
 * @details This binds a given event handler (a function taking the event as the
 *   first argument) to an event name. Whenever the event gets triggered, the
 *   event handler will get invoked.
 *
 *   In case the event is already bound, a warning is printed.
 *
 * @param event_name Name of the event to bind to
 * @param callback Event handler, a method taking only one argument (the event)
 */
INLINE void LUIBaseElement::bind(const string& event_name, CallbackObject* callback) {
  if (_events.count(event_name) != 0) {
    lui_cat.warning() << "Overriding event handler for '" << event_name << "', target = " << _debug_name << endl;
  }
  _events[event_name] = callback;
}

/**
 * @brief Unbinds an event handler
 * @details Unbinds a event handler, in case one is bound to the given event.
 *   If there was no event handler for the given event, a warning is printed, and
 *   nothing happens.
 *
 * @param event_name Name of the event to unbind the handler for
 */
INLINE void LUIBaseElement::unbind(const string& event_name) {
  const auto elem_it = _events.find(event_name);
  if (elem_it != _events.end()) {
    _events.erase(elem_it);
  } else {
    lui_cat.warning() << "Unbinding event handler for '" << event_name << "', but none was ever set!" << endl;
  }
}

/**
 * @brief Unbinds all events
 * @details This unbinds the element from all events, effectively calling unbind()
 *   for every registered event. You should be careful on this, since most builtin
 *   events will rely on certain events to be bound to them.
 */
INLINE void LUIBaseElement::unbind_all() {
  _events.clear();
}

/**
 * @brief Checks whether an event handler is bound to the given event
 * @details This checks whether there is a event handler for the event.
 *   Returns true if there is a handler bound to the event, otherwise false.
 *
 * @param event_name Name of the evenet
 * @return true if the event has an event handler, false otherwise
 */
INLINE bool LUIBaseElement::has_event(const string& event_name) {
  return _events.count(event_name) > 0;
}

/**
 * @brief Sets the elements name
 * @details This sets the name of the element, which can get queried by get_name
 *   later on. This does not expose any functionality, and only is a help for the
 *   user.
 *
 * @param name Name of the element
 */
INLINE void LUIBaseElement::set_name(const string& name) {
  _name = name;
}

/**
 * @brief Returns the name of the element
 * @details Returns the name of the element, or an empty string if no name
 *   was set yet.
 *
 * @return Name of the element
 */
INLINE const string& LUIBaseElement::get_name() const {
  return _name;
}

/**
 * @brief Sets whether to snap the position
 * @details This controls whether the element snaps it position to the pixel grid.
 *   If this is true, ceil() will be called on the position and size. This prevents
 *   the element from being on subpixel positions, and thus causing artifacts
 *   (for example, gaps).
 *
 * @param snap true to make the element snap, false otherwise
 */
INLINE void LUIBaseElement::set_snap_position(bool snap) {
  _snap_position = snap;
}

/**
 * @brief Sets the top left position
 * @details This makes the element aligned top/left and sets its position relative
 *   to that corner.
 *
 * @param pos Distance to the top-left corner
 */
INLINE void LUIBaseElement::set_top_left(const LPoint2& pos) {
  _placement.x = M_default;
  _placement.y = M_default;
  _position = pos;
}

/**
 * @brief Sets the top right position
 * @details This makes the element aligned top/right and sets its position relative
 *   to that corner.
 *
 * @param pos Distance to the top-right corner
 */
INLINE void LUIBaseElement::set_top_right(const LPoint2& pos) {
  _placement.x = M_inverse;
  _placement.y = M_default;
  _position = pos;
}

/**
 * @brief Sets the bottom left position
 * @details This makes the element aligned bottom/left and sets its position relative
 *   to that corner.
 *
 * @param pos Distance to the bottom-öeft corner
 */
INLINE void LUIBaseElement::set_bottom_left(const LPoint2& pos) {
  _placement.x = M_default;
  _placement.y = M_inverse;
  _position = pos;
}

/**
 * @brief Sets the bottom right position
 * @details This makes the element aligned bottom/right and sets its position relative
 *   to that corner.
 *
 * @param pos Distance to the bottom-right corner
 */
INLINE void LUIBaseElement::set_bottom_right(const LPoint2& pos) {
  _placement.x = M_inverse;
  _placement.y = M_inverse;
  _position = pos;
}

/**
 * @brief Returns the distance to the top left corner
 * @details This returns the distance to the top left corner. The returned value
 *   is only meaningful if the elment is aligned top left.
 * @return Distance to the top left corner
 */
INLINE LPoint2 LUIBaseElement::get_top_left() const {
  return LPoint2(get_left(), get_top());
}

/**
 * @brief Returns the distance to the top right corner
 * @details This returns the distance to the top right corner. The returned value
 *   is only meaningful if the elment is aligned top right.
 * @return Distance to the top right corner
 */
INLINE LPoint2 LUIBaseElement::get_top_right() const {
  return LPoint2(get_right(), get_top());
}

/**
 * @brief Returns the distance to the bottom left corner
 * @details This returns the distance to the bottom left corner. The returned value
 *   is only meaningful if the elment is aligned bottom left.
 * @return Distance to the bottom left corner
 */
INLINE LPoint2 LUIBaseElement::get_bottom_left() const {
  return LPoint2(get_left(), get_bottom());
}

/**
 * @brief Returns the distance to the bottom right corner
 * @details This returns the distance to the bottom right corner. The returned value
 *   is only meaningful if the elment is aligned bottom right.
 * @return Distance to the bottom right corner
 */
INLINE LPoint2 LUIBaseElement::get_bottom_right() const {
  return LPoint2(get_right(), get_bottom());
}

/**
 * @brief Sets the top left position
 * @details This is an alias for LUIBaseElement::set_top_left()
 *
 * @param pos See LUIBaseElement::set_top_left()
 */
INLINE void LUIBaseElement::set_pos(const LPoint2& pos) {
  set_pos(pos.get_x(), pos.get_y());
}

/**
 * @brief Sets the top left position
 * @details This is an alias for LUIBaseElement::set_top_left()
 *
 * @param x See LUIBaseElement::set_top_left()
 * @param y See LUIBaseElement::set_top_left()
 */
INLINE void LUIBaseElement::set_pos(float x, float y) {
  set_top_left(LPoint2(x, y));
}

/**
 * @brief Returns the top left position
 * @details This is an alias for LUIBaseElement::get_top_left().
 * @return Top left position
 */
INLINE LPoint2 LUIBaseElement::get_pos() const {
  return get_top_left();
}

/**
 * @brief Returns the elements absolute position.
 * @details This returns the last frame absolute position of the element.
 *   You should not rely on this method to return correct values, since it is
 *   only valid after at least one frame has been rendered.
 * @return Absolute position in pixels of the element
 */
INLINE LPoint2 LUIBaseElement::get_abs_pos() const {
  return _abs_position;
}

/**
 * @brief Sets the top position of the element
 * @details This makes the element aligned to the top, and sets the distance
 *   to the top.
 *
 * @param top Distance to the top
 */
INLINE void LUIBaseElement::set_top(float top) {
  _placement.y = M_default;
  _position.set_y(top);
}

/**
 * @brief Sets the right position of the element
 * @details This makes the element aligned to the right, and sets the distance
 *   to the right.
 *
 * @param right Distance to the right
 */
INLINE void LUIBaseElement::set_right(float right) {
  _placement.x = M_inverse;
  _position.set_x(right);
}

/**
 * @brief Sets the bottom position of the element
 * @details This makes the element aligned to the bottom, and sets the distance
 *   to the bottom.
 *
 * @param bottom Distance to the bottom
 */
INLINE void LUIBaseElement::set_bottom(float bottom) {
  _placement.y = M_inverse;
  _position.set_y(bottom);
}

/**
 * @brief Sets the left position of the element
 * @details This makes the element aligned to the left, and sets the distance
 *   to the left.
 *
 * @param left Distance to the right
 */
INLINE void LUIBaseElement::set_left(float left) {
  _placement.x = M_default;
  _position.set_x(left);
}

/**
 * @brief Returns the distance to the top
 * @details This returns the distance to the top. This value is only meaningful
 *   if the element is aligned to the top.
 *
 * @return Distance to the top.
 */
INLINE float LUIBaseElement::get_top() const {
  return _position.get_y();
}

/**
 * @brief Returns the distance to the right
 * @details This returns the distance to the right. This value is only meaningful
 *   if the element is aligned to the right.
 *
 * @return Distance to the right.
 */
INLINE float LUIBaseElement::get_right() const {
  return _position.get_x();
}

/**
 * @brief Returns the distance to the bottom
 * @details This returns the distance to the bottom. This value is only meaningful
 *   if the element is aligned to the bottom.
 *
 * @return Distance to the bottom.
 */
INLINE float LUIBaseElement::get_bottom() const {
  return _position.get_y();
}

/**
 * @brief Returns the distance to the left
 * @details This returns the distance to the left. This value is only meaningful
 *   if the element is aligned to the left.
 *
 * @return Distance to the left.
 */
INLINE float LUIBaseElement::get_left() const {
  return _position.get_x();
}

/**
 * @brief Sets whether to center the element
 * @details This method controls whether to center the element horizontally
 *   or vertically. When passing false to either center_vert or center_horiz,
 *   nothing in that direction happens.
 *
 *   For example:
 *     set_centered(true, false) makes the element center vertically,
 *     but keep its horizontal position.
 *
 *     set_centered(false, true) makes the element center horizontally,
 *     but keep its vertical position.
 *
 *     set_centered(true, true) makes the element center in both dimensions
 *
 *   However, set_centered(false, false) emits a warning, since it effectively
 *   does nothing.
 *
 * @param center_vert Whether to center the element vertically
 * @param center_horiz Whether to center the element horizontally
 */
INLINE void LUIBaseElement::set_centered(bool center_vert, bool center_horiz) {
  if (center_horiz) {
    _placement.x = M_center;
    _position.set_x(0.0f);
  }

  if (center_vert) {
    _placement.y = M_center;
    _position.set_y(0.0f);
  }

  if (!center_vert && !center_horiz) {
    luiBaseElement_cat.warning() << "set_centered() called, but no parameter was true. To un-center an "
                                 << "element, use the top_left property for example instead." << endl;
  }
}

/**
 * @brief Sets whether to center the element vertically
 * @details This makes the element center vertically. If centered is set to false,
 *   a warning is printed. The centered parameter only exists to be able to do
 *   element.center_vertical = True in python. The parameter should never be
 *   false. To un-center an element, instead call set_top or set_bottom.
 *
 * @param centered Should always be true
 */
INLINE void LUIBaseElement::set_center_vertical(bool centered) {
  if (centered) {
    _placement.y = M_center;
    _position.set_y(0.0f);
  } else {
    luiBaseElement_cat.warning() << "set_center_vertical called with false as argument, this has no effect!" << endl;
  }
}

/**
 * @brief Sets whether to center the element horizontally
 * @details This makes the element center horizontally. If centered is set to false,
 *   a warning is printed. The centered parameter only exists to be able to do
 *   element.center_horizontal = True in python. The parameter should never be
 *   false. To un-center an element, instead call set_left or set_right.
 *
 * @param centered Should always be true
 */
INLINE void LUIBaseElement::set_center_horizontal(bool centered) {
  if (centered) {
    _placement.x = M_center;
    _position.set_x(0.0f);
  } else {
    luiBaseElement_cat.warning() << "set_center_horizontal called with false as argument, this has no effect!" << endl;
  }
}

/**
 * @brief Returns whether the element is centered
 * @details This returns whether the element is horizontally and vertically
 *   centered.
 *
 * @return true if the element is centered, false otherweise
 */
INLINE bool LUIBaseElement::is_centered() const {
  return _placement.x == M_center && _placement.y == M_center;
}

/**
 * @brief Returns whether the element is vertically centered
 * @details This returns whether the element is vertically centered.
 * @return true if the element is vertically centered
 */
INLINE bool LUIBaseElement::is_vertical_centered() const {
  return _placement.y == M_center;
}


/**
 * @brief Returns whether the element is horizontally centered
 * @details This returns whether the element is horizontally centered.
 * @return true if the element is horizontally centered
 */
INLINE bool LUIBaseElement::is_horizontal_centered() const {
  return _placement.x == M_center;
}

/**
 * @brief Sets the margin of the element
 * @details This sets the margin of the element. The margin should be stored in
 *   the order top, right, bottom, left (as in CSS, TRouBLe). The margin controls
 *   the distance to the sides, and behaves just like in CSS.
 *
 * @param margin Margin in pixels, top, right, bottom, left
 */
INLINE void LUIBaseElement::set_margin(const LVector4& margin) {
  _margin.set_bounds(margin);
}

/**
 * @brief Sets the margin of the element
 * @details This sets the margin of the element. The margin controls the distance
 *   to the sides, and behaves just like in CSS:
 *
 * @param top Margin to the top
 * @param right Margin to the right
 * @param bottom Margin to the bottom
 * @param left Margin to the left
 */
INLINE void LUIBaseElement::set_margin(float top, float right, float bottom, float left) {
  _margin.set_bounds(top, right, bottom, left);
}

/**
 * @brief Sets the margin of the element
 * @details Sets an equal margin to all sides of the element, this is equal to
 *   calling LUIBaseElement::set_margin(margin, margin, margin, margin).
 *
 * @param margin Margin to all sides
 */
INLINE void LUIBaseElement::set_margin(float margin) {
  _margin.set_bounds(margin, margin, margin, margin);
}

/**
 * @brief Sets the top-margin
 * @details This sets only the top-margin, see LUIBaseElement::set_margin()
 *
 * @param top Margin to the top
 */
INLINE void LUIBaseElement::set_margin_top(float top) {
  _margin.set_top(top);
}

/**
 * @brief Sets the right-margin
 * @details This sets only the right-margin, see LUIBaseElement::set_margin()
 *
 * @param right Margin to the right
 */
INLINE void LUIBaseElement::set_margin_right(float right) {
  _margin.set_right(right);
}

/**
 * @brief Sets the bottom-margin
 * @details This sets only the bottom-margin, see LUIBaseElement::set_margin()
 *
 * @param bottom Margin to the bottom
 */
INLINE void LUIBaseElement::set_margin_bottom(float bottom) {
  _margin.set_bottom(bottom);
}

/**
 * @brief Sets the left-margin
 * @details This sets only the left-margin, see LUIBaseElement::set_margin()
 *
 * @param left Margin to the left
 */
INLINE void LUIBaseElement::set_margin_left(float left) {
  _margin.set_left(left);
}

/**
 * @brief Returns the margin to the top
 * @details This returns the margin to the top
 * @return Margin to the top
 */
INLINE float LUIBaseElement::get_margin_top() const {
  return _margin.get_top();
}

/**
 * @brief Returns the margin to the right
 * @details This returns the margin to the right
 * @return Margin to the right
 */
INLINE float LUIBaseElement::get_margin_right() const {
  return _margin.get_right();
}

/**
 * @brief Returns the margin to the bottom
 * @details This returns the margin to the bottom
 * @return Margin to the bottom
 */
INLINE float LUIBaseElement::get_margin_bottom() const {
  return _margin.get_bottom();
}

/**
 * @brief Returns the margin to the left
 * @details This returns the margin to the left
 * @return Margin to the left
 */
INLINE float LUIBaseElement::get_margin_left() const {
  return _margin.get_left();
}

/**
 * @brief Returns the margin of the element.
 * @details This returns the margin of the element. This method returns a non-const
 *   reference, thus .get_margin().set_top(123) is perfectly fine. This is mainly
 *   to support property chaining in python, so the user can do .margin.left = 5
 * @return Handle to the margin bounds
 */
INLINE LUIBounds& LUIBaseElement::get_margin() {
  return _margin;
}

/**
 * @brief Returns the margin of the element
 * @details This returns the margin of the element, as const-version, so the bounds
 *   are read-only.
 * @return Readonly handle to the margin bounds
 */
INLINE const LUIBounds& LUIBaseElement::get_margin() const {
  return _margin;
}

/**
 * @brief Sets the padding of the element
 * @details This sets the padding of the element. The padding should be stored in
 *   the order top, right, bottom, left (as in CSS, TRouBLe). The padding controls
 *   the distance to the sides, and behaves just like in CSS.
 *
 * @param padding padding in pixels, top, right, bottom, left
 */
INLINE void LUIBaseElement::set_padding(const LVector4& padding) {
  _padding.set_bounds(padding);
}

/**
 * @brief Sets the padding of the element
 * @details This sets the padding of the element. The padding controls the distance
 *   to the sides, and behaves just like in CSS:
 *
 * @param top padding to the top
 * @param right padding to the right
 * @param bottom padding to the bottom
 * @param left padding to the left
 */
INLINE void LUIBaseElement::set_padding(float top, float right, float bottom, float left) {
  _padding.set_bounds(top, right, bottom, left);
}

/**
 * @brief Sets the padding of the element
 * @details Sets an equal padding to all sides of the element, this is equal to
 *   calling LUIBaseElement::set_padding(padding, padding, padding, padding).
 *
 * @param padding padding to all sides
 */
INLINE void LUIBaseElement::set_padding(float padding) {
  _padding.set_bounds(padding, padding, padding, padding);
}

/**
 * @brief Sets the top-padding
 * @details This sets only the top-padding, see LUIBaseElement::set_padding()
 *
 * @param top padding to the top
 */
INLINE void LUIBaseElement::set_padding_top(float top) {
  _padding.set_top(top);
}

/**
 * @brief Sets the right-padding
 * @details This sets only the right-padding, see LUIBaseElement::set_padding()
 *
 * @param right padding to the right
 */
INLINE void LUIBaseElement::set_padding_right(float right) {
  _padding.set_right(right);
}

/**
 * @brief Sets the bottom-padding
 * @details This sets only the bottom-padding, see LUIBaseElement::set_padding()
 *
 * @param bottom padding to the bottom
 */
INLINE void LUIBaseElement::set_padding_bottom(float bottom) {
  _padding.set_bottom(bottom);
}

/**
 * @brief Sets the left-padding
 * @details This sets only the left-padding, see LUIBaseElement::set_padding()
 *
 * @param left padding to the left
 */
INLINE void LUIBaseElement::set_padding_left(float left) {
  _padding.set_left(left);
}

/**
 * @brief Returns the padding to the top
 * @details This returns the padding to the top
 * @return padding to the top
 */
INLINE float LUIBaseElement::get_padding_top() const {
  return _padding.get_top();
}

/**
 * @brief Returns the padding to the right
 * @details This returns the padding to the right
 * @return padding to the right
 */
INLINE float LUIBaseElement::get_padding_right() const {
  return _padding.get_right();
}

/**
 * @brief Returns the padding to the bottom
 * @details This returns the padding to the bottom
 * @return padding to the bottom
 */
INLINE float LUIBaseElement::get_padding_bottom() const {
  return _padding.get_bottom();
}

/**
 * @brief Returns the padding to the left
 * @details This returns the padding to the left
 * @return padding to the left
 */
INLINE float LUIBaseElement::get_padding_left() const {
  return _padding.get_left();
}

/**
 * @brief Returns the padding of the element.
 * @details This returns the padding of the element. This method returns a non-const
 *   reference, thus .get_padding().set_top(123) is perfectly fine. This is mainly
 *   to support property chaining in python, so the user can do .padding.left = 5
 * @return Handle to the padding bounds
 */
INLINE LUIBounds& LUIBaseElement::get_padding() {
  return _padding;
}

/**
 * @brief Returns the padding of the element
 * @details This returns the padding of the element, as const-version, so the bounds
 *   are read-only.
 * @return Readonly handle to the padding bounds
 */
INLINE const LUIBounds& LUIBaseElement::get_padding() const {
  return _padding;
}

/**
 * @brief Sets the size of the element
 * @details This sets the size of the element. Size can be either floats, determining
 *  the size in pixels, or valid terms for a LUIExpression, e.g. "23%".
 *
 * @param size width and height of the element
 */
INLINE void LUIBaseElement::set_size(const LVector2& size) {
  set_size(size.get_x(), size.get_y());
}

/**
 * @brief Sets the size of the element
 * @details This sets the size of the element. Size can be either floats, determining
 *  the size in pixels, or valid terms for a LUIExpression, e.g. "23%".
 *
 * @param width width of the element
 * @param height height of the element
 */
INLINE void LUIBaseElement::set_size(float width, float height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

/**
 * @brief Sets the size of the element
 * @details This sets the size of the element. Size can be either floats, determining
 *  the size in pixels, or valid terms for a LUIExpression, e.g. "23%".
 *
 * @param width width of the element
 * @param height height of the element
 */
INLINE void LUIBaseElement::set_size(const string& width, const string& height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

/**
 * @brief Sets the size of the element
 * @details This sets the size of the element. Size can be either floats, determining
 *  the size in pixels, or valid terms for a LUIExpression, e.g. "23%".
 *
 * @param width width of the element
 * @param height height of the element
 */
INLINE void LUIBaseElement::set_size(const string& width, float height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

/**
 * @brief Sets the size of the element
 * @details This sets the size of the element. Size can be either floats, determining
 *  the size in pixels, or valid terms for a LUIExpression, e.g. "23%".
 *
 * @param width width of the element
 * @param height height of the element
 */
INLINE void LUIBaseElement::set_size(float width, const string& height) {
  _size.x.load_expression(width);
  _size.y.load_expression(height);
}

/**
 * @brief Returns whether the element has a size assigned
 * @details This returns whether has_width() and has_height() are both true.
 * @return True if the element has a size for both dimensions.
 */
INLINE bool LUIBaseElement::has_size() const {
  return _size.x.has_expression() && _size.y.has_expression();
}

/**
 * @brief Returns whether the element has a width expression
 * @details This checks whether there was a width set on the element, either
 *   a fixed width in pixels, or a percentage width.
 * @return true if the element has a width assigned, false otherwise
 */
INLINE bool LUIBaseElement::has_width() const {
  return _size.x.has_expression();
}

/**
 * @brief Returns whether the element has a height expression
 * @details This checks whether there was a height set on the element, either
 *   a fixed height in pixels, or a percentage height
 * @return true if the element has a height assigned, false otherwise
 */
INLINE bool LUIBaseElement::has_height() const {
  return _size.y.has_expression();
}

/**
 * @brief Clears the elements width
 * @details This clears the elements width expression, clearing anything set
 *   with set_width() before.
 */
INLINE void LUIBaseElement::clear_width() {
  _size.x.clear();
}

/**
 * @brief Clears the elements height
 * @details This clears the elements height expression, clearing anything set
 *   with set_height() before.
 */
INLINE void LUIBaseElement::clear_height() {
  _size.y.clear();
}

/**
 * @brief Clears the elements size
 * @details This clears the elements size, calling clear_width() and clear_height().
 */
INLINE void LUIBaseElement::clear_size() {
  _size.x.clear();
  _size.y.clear();
}

/**
 * @brief Sets the width of the element
 * @details This sets the width of the element, width can either be a float
 *   determining the size in pixels, or a valid term for a LUIExpression, e.g. "23%".
 *
 * @param width Width of the element
 */
INLINE void LUIBaseElement::set_width(float width) {
  _size.x.load_expression(width);
}

/**
 * @brief Sets the width of the element
 * @details This sets the width of the element, width can either be a float
 *   determining the size in pixels, or a valid term for a LUIExpression, e.g. "23%".
 *
 * @param width Width of the element
 */
INLINE void LUIBaseElement::set_width(const string& width) {
  _size.x.load_expression(width);
}

/**
 * @brief Sets the height of the element
 * @details This sets the height of the element, height can either be a float
 *   determining the size in pixels, or a valid term for a LUIExpression, e.g. "23%".
 *
 * @param height Height of the element
 */
INLINE void LUIBaseElement::set_height(float height) {
  _size.y.load_expression(height);
}

/**
 * @brief Sets the height of the element
 * @details This sets the height of the element, height can either be a float
 *   determining the size in pixels, or a valid term for a LUIExpression, e.g. "23%".
 *
 * @param height Height of the element
 */
INLINE void LUIBaseElement::set_height(const string& height) {
  _size.y.load_expression(height);
}

/**
 * @brief Returns the width of the element
 * @details This returns an approximated width of the element. In case a fixed
 *   size was set on the element, it returns those. Otherwise it approximates
 *   the width using the last-frame width.
 * @return Approximated width
 */
INLINE float LUIBaseElement::get_width() const {
  if (_size.x.has_fixed_expression()) return _size.x.evaluate(0.0f);
  return _effective_size.get_x();
}

/**
 * @brief Returns the height of the element
 * @details This returns an approximated height of the element. In case a fixed
 *   size was set on the element, it returns those. Otherwise it approximates
 *   the height using the last-frame height.
 * @return Approximated width
 */
INLINE float LUIBaseElement::get_height() const {
  if (_size.y.has_fixed_expression()) return _size.y.evaluate(0.0f);
  return _effective_size.get_y();
}

/**
 * @brief Returns the size of the element
 * @details This returns an approximated size of the element. In case a fixed
 *   size was set on the element, it returns those. Otherwise it approximates
 *   the size using the last-frame size.
 * @return Approximated width
 */
INLINE LVector2 LUIBaseElement::get_size() const {
  return LVector2(get_width(), get_height());
}

/**
 * @brief Sets whether the element is visible
 * @details This sets the element visible. If visible is set to false, the element
 *   will not be rendered anymore. If visible is set to true, the element
 *   will be shown.
 *
 *   If any of the objects parents is hidden, this method has no effect, and the
 *   element will always be hidden,
 *
 * @param visible Whether to render the element
 */
INLINE void LUIBaseElement::set_visible(bool visible) {
  _visible = visible;
}

/**
 * @brief Returns whether the element is explicitly hidden or shown.
 * @details This returns the value previously set by set_visible(). It does
 *   *not* take into account whether any of the parents of the object is visible
 *   or not, so you cannot use this to determine whether the element was actually
 *   rendered or not.
 * @return Whether the element was explicitly hidden / shown
 */
INLINE bool LUIBaseElement::is_visible() const {
  return _visible;
}

/**
 * @brief Hides the element
 * @details This is an alias for set_visible(false)
 */
INLINE void LUIBaseElement::hide() {
  set_visible(false);
}

/**
 * @brief Shows the element
 * @details This is an alias for set_visible(true)
 */
INLINE void LUIBaseElement::show() {
  set_visible(true);
}

/**
 * @brief Returns the z offset of the element
 * @details This returns the z offset previously set with set_z_offset()
 * @return z offset of the element
 */
INLINE float LUIBaseElement::get_z_offset() const {
  return _z_offset;
}

/**
 * @brief Returns whether the element is focused
 * @details This method returns whether the element currently is focused.
 *   This is usually true after a call to request_focus()
 * @return [description]
 */
INLINE bool LUIBaseElement::has_focus() const {
  return _focused;
}

/**
 * @brief Returns whether the element has a parent
 * @details This method returns whether the element is currently parented to anything
 * @return true if a parent is set, false otherwise
 */
INLINE bool LUIBaseElement::has_parent() const {
  return _parent != nullptr;
}

/**
 * @brief Returns a handle to the parent
 * @details This returns a handle to the elements parent, or nullptr if no parent
 *   is present.
 * @return Handle to the parent
 */
INLINE LUIObject* LUIBaseElement::get_parent() const {
  return _parent;
}

/**
 * @brief Checks if the element intersects with a point
 * @details This checks if the element intersects with a given *absolute*
 *   coordinate point. This is only valid after traversing the tree, since otherwise
 *   the absolute position is not known.
 *
 * @param x absolute x-coordinate in pixels
 * @param y absolute y-coordinate in pixels
 *
 * @return true if the coordinate intersects with the element, false otherwise
 */
INLINE bool LUIBaseElement::intersects(float x, float y) const {
  return (
      x >= _abs_position.get_x() &&
      y >= _abs_position.get_y() &&
      x <= _abs_position.get_x() + _effective_size.get_x() &&
      y <= _abs_position.get_y() + _effective_size.get_y() &&

      x >= _abs_clip_bounds.get_x() &&
      y >= _abs_clip_bounds.get_y() &&
      x <= _abs_clip_bounds.get_x() + _abs_clip_bounds.get_w() &&
      y <= _abs_clip_bounds.get_y() + _abs_clip_bounds.get_h()
    );
}

/**
 * @brief Clears the clip bounds
 * @details This clears any clip bounds previously set with set_clip_bounds(),
 *   and thus makes the element not clip anymore.
 */
INLINE void LUIBaseElement::clear_clip_bounds() {
  _have_clip_bounds = false;
  _clip_bounds.set_bounds(0, 0, 0, 0);
}

/**
 * @brief Sets the elements clip bounds
 * @details This sets the elements clip bounds. This is equal to setting
 *   'overflow: hidden' in CSS. In case the clip bounds are (0, 0, 0, 0),
 *   the clipping will happen at the sides of the element. The bounds specify
 *   the distance of the clipping rect from the sides.
 *
 * @param bounds Distance of the clipping rect from the sides
 */
INLINE void LUIBaseElement::set_clip_bounds(const LUIBounds& bounds) {
  _clip_bounds = bounds;
  _have_clip_bounds = true;
}

/**
 * @brief Sets the elements clip bounds
 * @details This sets the elements clip bounds. This is equal to setting
 *   'overflow: hidden' in CSS. In case the clip bounds are (0, 0, 0, 0),
 *   the clipping will happen at the sides of the element. The bounds specify
 *   the distance of the clipping rect from the sides.
 *
 * @param top Distance of the clipping rect from the top
 * @param right Distance of the clipping rect from the right
 * @param bottom Distance of the clipping rect from the bottom
 * @param left Distance of the clipping rect from the left
 */
INLINE void LUIBaseElement::set_clip_bounds(float top, float right, float bottom, float left) {
  _clip_bounds.set_bounds(top, right, bottom, left);
  _have_clip_bounds = true;
}

/**
 * @brief Returns the clip bounds
 * @details This returns the clip bounds. In case no clip bounds were set, this
 *   returns (0, 0, 0, 0).
 * @return Current clip bounds
 */
INLINE const LUIBounds& LUIBaseElement::get_clip_bounds() const {
  return _clip_bounds;
}

/**
 * @brief Returns the clip rect
 * @details This returns the clip region, in absolute coordinate space. This is only
 *   valid after a frame has been rendered.
 * @return Absolute clip rectangle
 */
INLINE const LUIRect& LUIBaseElement::get_abs_clip_bounds() const {
  return _abs_clip_bounds;
}

/**
 * @brief Internal method to set the parent
 * @details This is the internal method used to set the current parent. It is used
 *   by the LUIObject after the object has been parented.
 *
 * @param parent The current parent
 */
INLINE void LUIBaseElement::do_set_parent(LUIObject* parent) {
  _parent = parent;
}

/**
 * @brief Internal method to set the focus
 * @details This is the internal method used to notify the element when it
 *   gained or lost focus. It just sets the new focus state
 *
 * @param focus Whether the element is currently focused
 */
INLINE void LUIBaseElement::set_focus(bool focus) {
  _focused = focus;
}

/**
 * @brief Returns the frame when the element was visible
 * @details This returns the index of the last frame where the element was visible
 *   and rendered. This can be used to determine if the element was rendered
 *   in the current frame or not, and is used by the event system.
 *
 * @return Last frame index where the element was visible
 */
INLINE int LUIBaseElement::get_last_frame_visible() const {
  return _last_frame_visible;
}

/**
 * @brief Returns whether the element is topmost
 * @details This returns whether the element is set to topmost, and thus gets
 *   rendered in front of all objects. This does not check if any parent of the
 *   object is topmost.
 *
 * @return True if the element is explicitly set to topmost
 */
INLINE bool LUIBaseElement::is_topmost() const {
  return _topmost;
}

/**
 * @brief Sets the element to render topmost
 * @details This makes the element render in top of all other elements. This also
 *   affects the children of the element in case it has some. Topmost elements are
 *   rendered in a seperate render pass above all elements. They also recieve
 *   events before regular events.
 *
 *   This does affect all children elements, too. Setting this too false will have
 *   no effect if any parent of the element is set to topmost.
 *
 * @param topmost Whether to render the element topmost
 */
INLINE void LUIBaseElement::set_topmost(bool topmost) {
  _topmost = topmost;
}

/**
 * @brief Returns the relative position of an absolute point
 * @details This returns the position of a point relative to this element. This is
 *   only valid after a frame has been rendered, since it depends on the absolute
 *   position. The relative position is computed by pos - element_pos.
 *
 * @param pos Absolute point position
 * @return Vector to that point, relative to the element
 */
INLINE LVector2 LUIBaseElement::get_relative_pos(const LPoint2& pos) const {
  return pos - _abs_position;
}

/**
 * @brief Returns the last render index of the element
 * @details This returns the last frames render index of the element. The render
 *   index is basically a counter which increases whenever an element gets
 *   rendered. This way the event manager can check if an element was rendered
 *   above an element, by doing a.render_index > b.render_index.
 *
 * @return Last frames render index
 */
INLINE int LUIBaseElement::get_last_render_index() const {
  return _last_render_index;
}

INLINE void LUIBaseElement::set_solid(bool solid) {
  _solid = solid;
  if (_solid) {
    register_events();
  } else {
    unregister_events();
  }
}

/**
 * @brief Returns whether element is solid
 * @details This returns the value previously set with set_solid(). See
 *   LUIBaseElement::set_solid() for further information.
 * @return Solidness of the element
 */
INLINE bool LUIBaseElement::get_solid() const {
  return _solid;
}

/**
 * @brief Returns the x-extent of the element
 * @details This returns the maximum x-position of the element. This can be
 *   used for fitting a parent to its children, by resizing so that all x- and
 *   y-extends are still contained.
 *
 *   The extend contains the margin as well as the size of the element.
 *
 * @return Maximum x-position of the element
 */
INLINE float LUIBaseElement::get_x_extent() const {
  return _abs_position.get_x() + _effective_size.get_x() + _margin.get_right();
}


/**
 * @brief Returns the y-extent of the element
 * @details This returns the maximum x-position of the element. This can be
 *   used for fitting a parent to its children, by resizing so that all x- and
 *   y-extends are still contained.
 *
 *   The extend contains the margin as well as the size of the element.
 *
 * @return Maximum y-position of the element
 */
INLINE float LUIBaseElement::get_y_extent() const {
  return _abs_position.get_y() + _effective_size.get_y() + _margin.get_bottom();
}

/**
 * @brief Sets the debugging name
 * @details This sets the debug name, which is shown when calling
 *   LUIBaseElement::ls(). It usually is set to the class name, but can be overriden
 *   to provide additional information.
 *
 * @param debug_name Debug-Name of the object.
 */
INLINE void LUIBaseElement::set_debug_name(const string& debug_name) {
  _debug_name = debug_name;
}

/**
 * @brief Returns the debugging name
 * @details This returns the debug name previously set with set_debug_name()
 * 
 * @return The debug name
 */
INLINE const string& LUIBaseElement::get_debug_name() const {
  return _debug_name;
}


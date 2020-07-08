import re

from LUIObject import LUIObject
from LUISprite import LUISprite
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState
from LUILayouts import LUIHorizontalStretchedLayout

__all__ = ["LUIInputField"]


class LUIInputField(LUIObject):

    """ Simple input field, accepting text input. This input field supports
    entering text and navigating. Selecting text is (currently) not supported.

    The input field also supports various keyboard shortcuts:

        [pos1]                  Move to the beginning of the text
        [end]                   Move to the end of the text
        [arrow_left]            Move one character to the left
        [arrow_right]           Move one character to the right
        [ctrl] + [arrow_left]   Move to the left, skipping over words
        [ctrl] + [arrow_right]  Move to the right, skipping over words
        [escape]                Un-focus input element

    """

    re_skip = re.compile("\W*\w+\W")

    def __init__(self, parent=None, width=200, placeholder=u"Enter some text ..", value=u"", **kwargs):
        """ Constructs a new input field. An input field always needs a width specified """
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self.set_width(width)
        self._layout = LUIHorizontalStretchedLayout(parent=self, prefix="InputField", width="100%")

        # Container for the text
        self._text_content = LUIObject(self)
        self._text_content.margin = (5, 7, 5, 7)
        self._text_content.clip_bounds = (0,0,0,0)
        self._text_content.set_size("100%", "100%")

        # Scroller for the text, so we can move right and left
        self._text_scroller = LUIObject(parent=self._text_content)
        self._text_scroller.center_vertical = True
        self._text = LUILabel(parent=self._text_scroller, text="")

        # Cursor for the current position
        self._cursor = LUISprite(self._text_scroller, "blank", "skin", x=0, y=0, w=2, h=15)
        self._cursor.color = (0.5, 0.5, 0.5)
        self._cursor.margin.top = 2
        self._cursor.z_offset = 20
        self._cursor_index = 0
        self._cursor.hide()
        self._value = value

        # Placeholder text, shown when out of focus and no value exists
        self._placeholder = LUILabel(parent=self._text_content, text=placeholder, shadow=False,
            center_vertical=True, alpha=0.2)

        # Various states
        self._tickrate = 1.0
        self._tickstart = 0.0

        self._render_text()

        if parent is not None:
            self.parent = parent

        LUIInitialState.init(self, kwargs)

    @property
    def value(self):
        """ Returns the value of the input field """
        return self._value

    @value.setter
    def value(self, new_value):
        """ Sets the value of the input field """
        self._value = new_value
        self._render_text()
        self.trigger_event("changed", self._value)

    def clear(self):
        """ Clears the input value """
        self.value = u""

    @property
    def cursor_pos(self):
        """ Set the cursor position """
        return self._cursor_index

    @cursor_pos.setter
    def cursor_pos(self, pos):
        """ Set the cursor position """
        if pos >= 0:
            self._cursor_index = max(0, min(len(self._value), pos))
        else:
            self._cursor_index = max(len(self._value) + pos + 1, 0)
        self._reset_cursor_tick()
        self._render_text()

    def on_tick(self, event):
        """ Tick handler, gets executed every frame """
        frame_time = globalClock.get_frame_time() - self._tickstart
        show_cursor = frame_time % self._tickrate < 0.5 * self._tickrate
        if show_cursor:
            self._cursor.color = (0.5, 0.5, 0.5, 1)
        else:
            self._cursor.color = (1, 1, 1, 0)

    def on_click(self, event):
        """ Internal on click handler """
        self.request_focus()

    def on_mousedown(self, event):
        """ Internal mousedown handler """
        local_x_offset = self._text.text_handle.get_relative_pos(event.coordinates).x
        self.cursor_pos = self._text.text_handle.get_char_index(local_x_offset)

    def _reset_cursor_tick(self):
        """ Internal method to reset the cursor tick """
        self._tickstart = globalClock.get_frame_time()

    def on_focus(self, event):
        """ Internal focus handler """
        self._cursor.show()
        self._placeholder.hide()
        self._reset_cursor_tick()
        self._layout.color = (0.9, 0.9, 0.9, 1)

    def on_keydown(self, event):
        """ Internal keydown handler. Processes the special keys, and if none are
        present, redirects the event """
        key_name = event.message
        if key_name == "backspace":
            self._value = self._value[:max(0, self._cursor_index - 1)] + self._value[self._cursor_index:]
            self.cursor_pos -= 1
            self.trigger_event("changed", self._value)
        elif key_name == "delete":
            post_value = self._value[min(len(self._value), self._cursor_index + 1):]
            self._value = self._value[:self._cursor_index] + post_value
            self.cursor_pos = self._cursor_index
            self.trigger_event("changed", self._value)
        elif key_name == "arrow_left":
            if event.get_modifier_state("alt") or event.get_modifier_state("ctrl"):
                self.cursor_skip_left()
            else:
                self.cursor_pos -= 1
        elif key_name == "arrow_right":
            if event.get_modifier_state("alt") or event.get_modifier_state("ctrl"):
                self.cursor_skip_right()
            else:
                self.cursor_pos += 1
        elif key_name == "escape":
            self.blur()
        elif key_name == "home":
            self.cursor_pos = 0
        elif key_name == "end":
            self.cursor_pos = len(self.value)

        self.trigger_event(key_name, self._value)

    def on_keyrepeat(self, event):
        """ Internal keyrepeat handler """
        self.on_keydown(event)

    def on_textinput(self, event):
        """ Internal textinput handler """
        self._value = self._value[:self._cursor_index] + event.message + \
            self._value[self._cursor_index:]
        self.cursor_pos = self._cursor_index + len(event.message)
        self.trigger_event("changed", self._value)

    def on_blur(self, event):
        """ Internal blur handler """
        self._cursor.hide()
        if len(self._value) < 1:
            self._placeholder.show()

        self._layout.color = (1, 1, 1, 1)

    def _render_text(self):
        """ Internal method to render the text """
        self._text.set_text(self._value)
        self._cursor.left = self._text.left + \
            self._text.text_handle.get_char_pos(self._cursor_index) + 1
        max_left = self.width - 15

        if self._value:
            self._placeholder.hide()
        else:
            if not self.focused:
                self._placeholder.show()

        # Scroll if the cursor is outside of the clip bounds
        rel_pos = self.get_relative_pos(self._cursor.get_abs_pos()).x
        if rel_pos >= max_left:
            self._text_scroller.left = min(0, max_left - self._cursor.left)
        if rel_pos <= 0:
            self._text_scroller.left = min(0, - self._cursor.left - rel_pos)

    def cursor_skip_left(self):
        """ Moves the cursor to the left, skipping the previous word """
        left_hand_str = ''.join(reversed(self.value[0:self.cursor_pos]))
        match = self.re_skip.match(left_hand_str)
        if match is not None:
            self.cursor_pos -= match.end() - 1
        else:
            self.cursor_pos = 0

    def cursor_skip_right(self):
        """ Moves the cursor to the right, skipping the next word """
        right_hand_str = self.value[self.cursor_pos:]
        match = self.re_skip.match(right_hand_str)
        if match is not None:
            self.cursor_pos += match.end() - 1
        else:
            self.cursor_pos = len(self.value)


from panda3d.core import LVecBase2i
from LUIObject import LUIObject
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

__all__ = ["LUIFormattedLabel"]


class LUIFormattedLabel(LUIObject):

    """ Small helper class to build a text consisting of different formatted
    parts of text. Uses LUILabels internally """

    def __init__(self, **kwargs):
        """ Creates a new formatted label. """
        LUIObject.__init__(self)
        LUIInitialState.init(self, kwargs)
        self._cursor = LVecBase2i(0)
        self._last_size = 14

    def clear(self):
        """ Removes all text from this label and resets it to the initial state.
        This will also detach the sub-labels from this label. """
        self._cursor.set(0, 0)
        self.remove_all_children()

    def newline(self, font_size=None):
        """ Moves the cursor to the next line. The font size controls how much
        the cursor will move. By default, the font size of the last added text
        is used, or if no text was added yet, a size of 14."""
        self._cursor.x = 0
        if font_size is None:
            font_size = self._last_size
        self._cursor.y += font_size + 2

    def add(self, *args, **kwargs):
        """ Appends a new text. The arguments are equal to the arguments of
        LUILabel. The arguments shouldn't contain information about the
        placement like top_left, or center_vertical, since the labels are
        placed at explicit positions. """
        self._last_size = kwargs.get("font_size", 14)
        label = LUILabel(parent=self, left=self._cursor.x, top=self._cursor.y,
                         *args, **kwargs)
        # This is a bit of a hack, we should use a horizontal layout, but we
        # don't for performance reasons.
        self._cursor.x += label.text_handle.width

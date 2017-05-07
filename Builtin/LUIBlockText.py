
from panda3d.core import LVecBase2i
from LUIObject import LUIObject
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

__all__ = ["LUIBlockText"]


class LUIBlockText(LUIObject):

    """ Small helper class to format labels into paragraphs.
    Uses LUILabels internally """

    def __init__(self, **kwargs):
        """ Creates a new block of text. """
        LUIObject.__init__(self)
        LUIInitialState.init(self, kwargs)
        self._cursor = LVecBase2i(0)
        self._last_size = 14

        self.labels = []


    def clear(self):
        """ Removes all text from this label and resets it to the initial state.
        This will also detach the sub-labels from this label. """
        self._cursor.set(0, 0)
        self.labels = []
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
        label = LUILabel(parent=self, left=self._cursor.x, top=self._cursor.y, width=self.get_width(),
                         *args, **kwargs)

        self.labels.append(label)

        # This is a bit of a hack, we should use a horizontal layout, but we
        # don't for performance reasons.
        self._cursor.y += label.text_handle.height

        # After every paragraph, we add a new line.
        self.newline()


    def set_text(self, text):
        """ Replaces the text with new text """
        self.clear()
        self.add(text=text)


    def update_height(self):
        """ Updates the height of the element, adding a newline to the end of
        every paragraph """
        top = 0
        for child in self.labels:
            child.top = top
            top += child._text.height
         
            # Newline
            top += self._last_size + 2


    def set_wrap(self, wrap):
        """ Sets text wrapping for the element.  Wrapping breaks lines on
        spaces, and breaks words if the word is longer than the line 
        length. """
        for child in self.children:
            for c in child.children:
                c.set_wordwrap(wrap)

        self.update_height()


    def set_width(self, width):
        """ Sets the width of this element, and turns on wrapping. """
        for child in self.children:
            child.set_width(width)
            
            # Need to force an update to the text when the width changes.
            for c in child.children:
                c.set_wordwrap(True)

        self.update_height()   

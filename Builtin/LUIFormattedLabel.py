
from panda3d.core import LVecBase2i
from panda3d.lui import LUIObject
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

    def clear(self):
        """ Removes all text from this label and resets it to the initial state """
        self._cursor.set(0, 0)
        self.remove_all_children()
        self.fit_to_children()

    def newline(self, font_size=14):
        """ Moves the cursor to the next line. The font size controlls how much
        the cursor will move. """
        self._cursor.x = 0
        self._cursor.y += font_size + 2

    def add(self, *args, **kwargs):
        """ Appends a new text. The arguments are equal to the arguments of
        LUILabel """
        label = LUILabel(parent=self,left=self._cursor.x, top=self._cursor.y, *args, **kwargs)
        self._cursor.x += label.width
        self.fit_to_children()

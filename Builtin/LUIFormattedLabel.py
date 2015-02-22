

from panda3d.lui import LUIObject
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

class LUIFormattedLabel(LUIObject):

    """ Small helper class to build a text consisting of different formatted
    parts text. Uses LUILabels """

    def __init__(self, **kwargs):
        """ Creates a new formatted label. """
        LUIObject.__init__(self)
        LUIInitialState.init(self, kwargs)
        self.currentLeft = 0
        self.currentTop = 0

    def clear(self):
        """ Removes all text from this label and resets it to the initial state """
        self.currentLeft = 0
        self.currentTop = 0
        self.remove_all_children()
        self.fit_to_children()

    def br(self, font_size=14):
        """ Moves the *cursor* to the next line """ 
        self.currentTop += font_size + 2
        self.currentLeft = 0

    def add_text(self, *args, **kwargs):
        """ Appends a new text. The arguments are equal to the arguments of 
        UILabel """
        label = LUILabel(parent=self,left=self.currentLeft, top=self.currentTop, *args, **kwargs)
        self.currentLeft += label.width
        self.fit_to_children()


from panda3d.lui import LUIObject, LUIText
from UIInitialState import UIInitialState

class UILabel(LUIObject):

    """ A simple label, displaying text. The text is shadowed by default. """
    
    def __init__(self, text=u"Label", shadow=True, font_size=14, font="label", **kwargs):
        """ Creates a new label. """
        LUIObject.__init__(self)
        UIInitialState.init(self, kwargs)
        self.text = LUIText(self, unicode(text), font, font_size, 0, 0)
        self.text.color = (1,1,1,0.9)
        self.text.z_offset = 1
        self.have_shadow = shadow

        if self.have_shadow:
            self.shadowText = LUIText(self, unicode(text), font, font_size, 0, 0)
            self.shadowText.top = 1
            self.shadowText.color = (0,0,0,0.7)

        self.fit_to_children()

    def get_text(self):
        """ Returns the current text of the label """
        return self.text.text

    def set_text(self, text):
        """ Changes the text of the label """
        self.text.text = unicode(text)
        if self.have_shadow:
            self.shadowText.text = unicode(text)
        self.fit_to_children()

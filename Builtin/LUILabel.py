
from panda3d.lui import LUIObject, LUIText
from LUIInitialState import LUIInitialState

__all__ = ["LUILabel"]

class LUILabel(LUIObject):

    """ A simple label, displaying text. """

    def __init__(self, text=u"Label", shadow=True, font_size=14, font="label", **kwargs):
        """ Creates a new label. If shadow is True, a small text shadow will be
        rendered below the actual text. """
        LUIObject.__init__(self)
        LUIInitialState.init(self, kwargs)
        self._text = LUIText(self, unicode(text), font, font_size)
        self._text.z_offset = 1
        self._have_shadow = shadow
        if self._have_shadow:
            self._shadow_text = LUIText(self, unicode(text), font, font_size)
            self._shadow_text.top = 1
            self._shadow_text.color = (0,0,0,0.6)

    def get_text_handle(self):
        """ Returns a handle to the internal used LUIText object """
        return self._text

    text_handle = property(get_text_handle)

    def get_text(self):
        """ Returns the current text of the label """
        return self._text.text

    def set_text(self, text):
        """ Sets the text of the label """
        self._text.text = unicode(text)
        if self._have_shadow:
            self._shadow_text.text = unicode(text)

    text = property(get_text, set_text)

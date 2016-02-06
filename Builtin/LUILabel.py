
from panda3d.lui import LUIObject, LUIText
from LUIInitialState import LUIInitialState

__all__ = ["LUILabel"]

class LUILabel(LUIObject):

    """ A simple label, displaying text. """

    DEFAULT_COLOR = (0.9, 0.9, 0.9, 1)
    DEFAULT_USE_SHADOW = True

    def __init__(self, text=u"Label", shadow=None, font_size=14, font="label", **kwargs):
        """ Creates a new label. If shadow is True, a small text shadow will be
        rendered below the actual text. """
        LUIObject.__init__(self)
        self._text = LUIText(self, unicode(text), font, font_size)
        self._text.z_offset = 1
        self.color = self.DEFAULT_COLOR
        if shadow is None:
            shadow = LUILabel.DEFAULT_USE_SHADOW
        self._have_shadow = shadow
        if self._have_shadow:
            self._shadow_text = LUIText(self, unicode(text), font, font_size)
            self._shadow_text.top = 1
            self._shadow_text.color = (0,0,0,0.6)
        LUIInitialState.init(self, kwargs)

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

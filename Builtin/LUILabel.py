
from panda3d.lui import LUIText
from LUIObject import LUIObject
from LUIInitialState import LUIInitialState

__all__ = ["LUILabel"]

class LUILabel(LUIObject):

    """ A simple label, displaying text. """

    # Default variables which can be overridden by skins
    DEFAULT_COLOR = (0.9, 0.9, 0.9, 1)
    DEFAULT_USE_SHADOW = True

    def __init__(self, text="Label", shadow=None, font_size=14, font="label", color=None, wordwrap=False, **kwargs):
        """ Creates a new label. If shadow is True, a small text shadow will be
        rendered below the actual text. """
        LUIObject.__init__(self)
        LUIInitialState.init(self, kwargs)
        self._text = LUIText(
            self,
            text,
            font,
            font_size,
            0,
            0,
            wordwrap
        )
        self._text.z_offset = 1
        if color is None:
            self.color = LUILabel.DEFAULT_COLOR
        else:
            self.color = color
        if shadow is None:
            shadow = LUILabel.DEFAULT_USE_SHADOW
        self._have_shadow = shadow
        if self._have_shadow:
            self._shadow_text = LUIText(
                self,
                text,
                font,
                font_size,
                0,
                0,
                wordwrap
            )
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
        self._text.text = text
        if self._have_shadow:
            self._shadow_text.text = text

    text = property(get_text, set_text)

    def get_color(self):
        """ Returns the current color of the label's text """
        return self._text.color

    def set_color(self, color):
        """ Sets the color of the label's text """
        self._text.color = color

    color = property(get_color, set_color)


from LUIObject import LUIObject
from LUILayouts import LUIHorizontalStretchedLayout
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

__all__ = ["LUIButton"]


class LUIButton(LUIObject):

    """ Simple button, containing three sprites and a label. """

    def __init__(self, text="Button", template="ButtonDefault", **kwargs):
        """ Constructs a new button. The template controls which sprites to use.
        If the template is "ButtonDefault" for example, the sprites
        "ButtonDefault_Left", "ButtonDefault" and "ButtonDefault_Right" will
        be used. The sprites used when the button is pressed should be named
        "ButtonDefaultFocus_Left" and so on then.

        If an explicit width is set on the button, the button will stick to
        that width, otherwise it will automatically resize to fit the label """
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self._template = template
        self._layout = LUIHorizontalStretchedLayout(
            parent=self, prefix=self._template, width="100%")
        self._label = LUILabel(parent=self, text=text)
        self._label.z_offset = 1
        self._label.center_vertical = True
        self._label.margin = 0, 20, 0, 20
        self.margin.left = -1
        LUIInitialState.init(self, kwargs)

    @property
    def text(self):
        """ Returns the current label text of the button """
        return self._label.text

    @text.setter
    def text(self, text):
        """ Sets the label text of the button """
        self._label.text = text

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self._layout.prefix = self._template + "Focus"
        self._label.margin.top = 1

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self._layout.prefix = self._template
        self._label.margin.top = 0

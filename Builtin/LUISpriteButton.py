
from LUIObject import LUIObject
from LUISprite import LUISprite
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

class LUISpriteButton(LUIObject):

    """ Simple button that uses only two images: Default and focus. """

    def __init__(self, template="ButtonDefault", **kwargs):
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self._template = template
        self._button_sprite = LUISprite(self, template, "skin")
        self._button_sprite.width = width
        self._button_sprite.height = height
        LUIInitialState.init(self, kwargs)

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self._button_sprite.set_texture(self.template + "Focus", "skin", resize=False)

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self._button_sprite.set_texture(self.template, "skin", resize=False)

    def on_click(self, event):
        """ Internal onclick handler. Do not override """
        self.trigger_event("changed")

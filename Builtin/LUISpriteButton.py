from panda3d.lui import LUIObject, LUISprite
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

class LUISpriteButton(LUIObject):

    """ Simple button that uses only two images: Default and focus. """
    def __init__(self, template="ButtonDefault", width = 50, height = 50, **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=0, h=0, solid=True)
        LUIInitialState.init(self, kwargs)
        self.margin_left = -1
        self.template = template

        self.fit_to_children()

        self.button_sprite = LUISprite(self, template, "skin")
        self.fit_to_children()

        self.width = width
        self.height = height

        self.button_sprite.width = width
        self.button_sprite.height = height

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self.button_sprite.set_texture(self.template + "Focus", "skin", resize=False)

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self.button_sprite.set_texture(self.template, "skin", resize=False)

    def on_click(self, event):
        """ Internal onclick handler. Do not override """
        self.trigger_event("changed")
        self._update_sprite()

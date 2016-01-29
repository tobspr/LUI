
from panda3d.lui import LUIObject, LUISprite
from LUIInitialState import LUIInitialState
from LUILabel import LUILabel

class LUIRadiobox(LUIObject):

    """ A radiobox which can be used in combination with a LUIRadioboxGroup """

    def __init__(self, group=None, value=None, active=False, label=u"Radiobox", **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=0, h=0, solid=True)
        LUIInitialState.init(self, kwargs)
        self._sprite = LUISprite(self, "Radiobox_Default", "skin")
        self._label = LUILabel(parent=self, text=label, shadow=True, left=self._sprite.width + 6)
        self._label.top = self._label.height - self._sprite.height
        self._label.bind("resized", self._on_label_resized)

        self.fit_to_children()
        self._group = group
        self._group.register_box(self)
        self._active = False
        self._value = value

        if active:
            self.set_active()

    def _on_label_resized(self, event):
        """ Internal handler when the text of the label got changed """
        self.fit_to_children()

    def on_click(self, event):
        """ Internal onclick handler. Do not override. """
        self.set_active()

    def set_active(self):
        """ Internal function to set the radiobox active """
        if self._group is not None:
            self._group.set_active_box(self)
        else:
            self._update_state(True)

    def get_value(self):
        """ Returns the value of the radiobox """
        return self._value

    def set_value(self, value):
        """ Sets the value of the radiobox """
        self._value = value

    value = property(get_value, set_value)

    def get_label(self):
        """ Returns a handle to the label, so it can be modified (e.g. change
            its text) """
        return self._label

    label = property(get_label)

    def _update_state(self, active):
        """ Internal method to update the state of the radiobox. Called by the
        LUIRadioboxGroup """
        self._active = active
        self.trigger_event("changed")
        self._update_sprite()

    def on_mousedown(self, event):
        """ Internal onmousedown handler. Do not override. """
        self.color = (0.86,0.86,0.86,1.0)

    def on_mouseup(self, event):
        """ Internal onmouseup handler. Do not override. """
        self.color = (1,1,1,1)

    def _update_sprite(self):
        """ Internal function to update the sprite of the radiobox """
        img = "Radiobox_Active" if self._active else "Radiobox_Default"
        self._sprite.set_texture(img, "skin")

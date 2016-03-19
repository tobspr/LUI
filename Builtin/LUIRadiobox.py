
from __future__ import division

from LUIObject import LUIObject
from LUISprite import LUISprite
from LUIInitialState import LUIInitialState
from LUILabel import LUILabel

class LUIRadiobox(LUIObject):

    """ A radiobox which can be used in combination with a LUIRadioboxGroup """

    def __init__(self, parent=None, group=None, value=None, active=False, label=u"Radiobox", **kwargs):
        """ Constructs a new radiobox. group should be a handle to a LUIRadioboxGroup.
        value will be the value returned by group.value, in case the box was
        selected. By default, the radiobox is not active. """
        assert group is not None, "LUIRadiobox needs a LUIRadioboxGroup!"
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self._sprite = LUISprite(self, "Radiobox_Default", "skin")
        self._label = LUILabel(parent=self, text=label, margin=(0, 0, 0, 23),
            center_vertical=True)
        self._value = value
        self._active = False
        self._hovered = False
        self._group = group
        self._group.register_box(self)
        if active:
            self.set_active()
        if parent:
            self.parent = parent
        LUIInitialState.init(self, kwargs)

    def on_click(self, event):
        """ Internal onclick handler. Do not override. """
        self.set_active()

    def on_mouseover(self, event):
        """ Internal mouseover handler """
        self._hovered = True
        self._update_sprite()

    def on_mouseout(self, event):
        """ Internal mouseout handler """
        self._hovered = False
        self._update_sprite()

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
        self._sprite.color = (0.86,0.86,0.86,1.0)

    def on_mouseup(self, event):
        """ Internal onmouseup handler. Do not override. """
        self._sprite.color = (1,1,1,1)

    def _update_sprite(self):
        """ Internal function to update the sprite of the radiobox """
        img = "Radiobox_Active" if self._active else "Radiobox_Default"
        if self._hovered:
            img += "Hover"
        self._sprite.set_texture(img, "skin")

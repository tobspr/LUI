
from __future__ import division

from panda3d.lui import LUIObject, LUISprite
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

__all__ = ["LUICheckbox"]

class LUICheckbox(LUIObject):

    """ This is a simple checkbox, including a Label. The checkbox can either
    be checked or unchecked. """

    def __init__(self, checked=False, label=u"Checkbox", **kwargs):
        """ Constructs a new checkbox with the given label and state. By default,
        the checkbox is not checked. """
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self._checked = checked
        self._checkbox_sprite = LUISprite(self, "Checkbox_Default", "skin")
        self._label = LUILabel(parent=self, text=label, shadow=True, margin=(-1, 0, 0, 23),
            center_vertical=True)
        self._hovered = False
        LUIInitialState.init(self, kwargs)

    def on_click(self, event):
        """ Internal onclick handler. Do not override """
        self._checked = not self._checked
        self.trigger_event("changed")
        self._update_sprite()

    def on_mousedown(self, event):
        """ Internal mousedown handler. """
        self._checkbox_sprite.color = (0.9, 0.9, 0.9, 1.0)

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. """
        self._checkbox_sprite.color = (1, 1, 1, 1)

    def on_mouseover(self, event):
        """ Internal mouseover handler """
        self._hovered = True
        self._update_sprite()

    def on_mouseout(self, event):
        """ Internal mouseout handler """
        self._hovered = False
        self._update_sprite()

    def toggle_checked(self):
        """ Toggles the checkbox state """
        self.checked = not self.checked

    def set_checked(self, checked):
        """ Sets the checkbox state """
        self._checked = checked
        self._update_sprite()

    def get_checked(self):
        """ Returns a boolean whether the checkbox is currently checked """
        return self._checked

    checked = property(get_checked, set_checked)

    def get_label(self):
        """ Returns a handle to the label, so it can be modified (e.g. changing
            its text) """
        return self._label

    label = property(get_label)

    def _update_sprite(self):
        """ Internal method to update the sprites """
        img = "Checkbox_Checked" if self._checked else "Checkbox_Default"
        if self._hovered:
            img += "Hover"
        self._checkbox_sprite.set_texture(img, "skin")

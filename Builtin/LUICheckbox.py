
from __future__ import division

from LUIObject import LUIObject
from LUISprite import LUISprite
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
        self._label = LUILabel(parent=self, text=label, margin=(0, 0, 0, 25),
                               center_vertical=True, alpha=0.4)
        self._hovered = False
        self._update_sprite()
        LUIInitialState.init(self, kwargs)

    @property
    def checked(self):
        """ Returns True if the checkbox is currently checked """
        return self._checked

    @checked.setter
    def checked(self, checked):
        """ Sets the checkbox state """
        self._checked = checked
        self._update_sprite()

    def toggle(self):
        """ Toggles the checkbox state """
        self.checked = not self.checked

    @property
    def label(self):
        """ Returns a handle to the label, so it can be modified """
        return self._label

    @property
    def sprite(self):
        """ Returns a handle to the internal checkbox sprite """
        return self._checkbox_sprite

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

    def _update_sprite(self):
        """ Internal method to update the sprites """
        img = "Checkbox_Checked" if self._checked else "Checkbox_Default"
        if self._hovered:
            img += "Hover"
        self._checkbox_sprite.set_texture(img, "skin")

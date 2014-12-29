
from panda3d.lui import LUIObject, LUISprite
from UILabel import UILabel
from UIInitialState import UIInitialState

class UICheckbox(LUIObject):

    """ This is a simple checkbox, including a Label. The checkbox can either
    be checked or unchecked. """

    def __init__(self, checked=False, label=u"Checkbox", **kwargs):
        """ Constructs a new checkbox with the given label and state. """
        LUIObject.__init__(self)
        UIInitialState.init(self, kwargs)
        self.checkboxSprite = LUISprite(self, "Checkbox_Default", "skin")
        self.label = UILabel(parent=self, text=label, shadow=True, left=self.checkboxSprite.width + 6)
        self.label.top = self.label.height - self.checkboxSprite.height
        self.fit_to_children()

        self.checked = checked
        self._update_sprite()

    def on_click(self, event):
        """ Internal onclick handler. Do not override """
        self.checked = not self.checked
        self.trigger_event("changed")
        self._update_sprite()

    def on_mousedown(self, event):
        """ Internal mousedown handler. Do not override """
        self.checkboxSprite.color = (0.86,0.86,0.86,1.0)

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self.checkboxSprite.color = (1,1,1,1)

    def get_checked(self):
        """ Returns a boolean wheter the checkbox is currently checked """
        return self.checked

    def set_checked(self, checked):
        """ Sets the checkbox state """
        self.checked = checked
        self._update_sprite()

    def get_label(self):
        """ Returns a handle to the label, so you can modify it (e.g. change 
            its text) """
        return self.label

    def _update_sprite(self):
        """ Internal method to update the sprites """
        img = "Checkbox_Checked" if self.checked else "Checkbox_Default"
        self.checkboxSprite.set_texture(img, "skin")

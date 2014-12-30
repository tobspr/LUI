
from panda3d.lui import LUIObject
from UILayouts import UIHorizontalStretchedLayout
from UILabel import UILabel
from UIInitialState import UIInitialState

class UIButton(LUIObject):

    """ Simple button. """
    def __init__(self, text=u"Button", template="ButtonDefault", **kwargs):
        LUIObject.__init__(self)
        UIInitialState.init(self, kwargs)
        self.dynamicWidth = "width" not in kwargs
        self.margin_left = -1
        self.template = template
        self.label = UILabel(parent=self, text=text, shadow=True, z_offset=1,
                                centered=(True, True), margin=(-3, 0, 0, -1))

        if self.dynamicWidth:
            width = int(self.label.width) + 15
        else:
            width = kwargs["width"]

        self.layout = UIHorizontalStretchedLayout(parent=self, width=width, prefix=self.template)
        self.fit_to_children()

    def set_text(self, text):
        """ Sets the text of the button """
        self.label.set_text(text)
        if self.dynamicWidth:
            self.width = int(self.label.width) + 15
            self.layout.width = self.width
            self.layout.recompute()

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self.layout.set_prefix(self.template + "Focus")
        self.label.margin_top = -2

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self.layout.set_prefix(self.template)
        self.label.margin_top = -3

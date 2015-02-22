
from panda3d.lui import LUIObject
from LUILayouts import LUIHorizontalStretchedLayout
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

class LUIButton(LUIObject):

    """ Simple button """
    def __init__(self, text=u"Button", template="ButtonDefault", **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=0, h=0, solid=True)
        LUIInitialState.init(self, kwargs)
        self.dynamicWidth = "width" not in kwargs
        self.margin_left = -1
        self.template = template
        self.label = LUILabel(parent=self, text=text, shadow=True, z_offset=1,
                                centered=(True, True), margin=(-3, 0, 0, -1))

        if self.dynamicWidth:
            width = int(self.label.width) + 20
        else:
            width = kwargs["width"]

        self.layout = LUIHorizontalStretchedLayout(parent=self, width=width, prefix=self.template)
        self.fit_to_children()

    def on_resized(self, event):
        """ Internal callback when the button gets resized """
        if not self.dynamicWidth:
            self.layout.width = self.width
            self.layout.recompute()

    def set_text(self, text):
        """ Sets the text of the button """
        self.label.set_text(text)
        if self.dynamicWidth:
            self.width = int(self.label.width) + 20

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self.layout.set_prefix(self.template + "Focus")
        self.label.margin_top = -2

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self.layout.set_prefix(self.template)
        self.label.margin_top = -3

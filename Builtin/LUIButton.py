
from panda3d.lui import LUIObject
from LUILayouts import LUIHorizontalStretchedLayout
from LUILabel import LUILabel
from LUIInitialState import LUIInitialState

class LUIButton(LUIObject):

    """ Simple button """

    def __init__(self, text=u"Button", template="ButtonDefault", **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=0, h=0, solid=True)
        self.margin_left = -1
        self._dynamic_width = "width" not in kwargs
        self._template = template
        self._label = LUILabel(parent=self, text=text, shadow=True, z_offset=1,
                                centered=(True, True), margin=(-3, 0, 0, -1))

        if self._dynamic_width:
            width = int(self._label.width) + 20
        else:
            width = kwargs["width"]

        self._layout = LUIHorizontalStretchedLayout(parent=self, width=width, prefix=self._template)
        self.fit_to_children()

        LUIInitialState.init(self, kwargs)

    def on_resized(self, event):
        """ Internal callback when the button gets resized """
        if not self._dynamic_width:
            self._layout.width = self.width
            self._layout.recompute()

    def set_text(self, text):
        """ Sets the text of the button """
        self._label.set_text(text)
        if self._dynamic_width:
            self.width = int(self._label.width) + 20

    def on_mousedown(self, event):
        """ Internal on_mousedown handler. Do not override """
        self._layout.set_prefix(self._template + "Focus")
        self._label.margin_top = -2

    def on_mouseup(self, event):
        """ Internal on_mouseup handler. Do not override """
        self._layout.set_prefix(self._template)
        self._label.margin_top = -3

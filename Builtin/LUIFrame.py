
from __future__ import print_function

from panda3d.lui import LUIObject
from LUILayouts import LUICornerLayout
from LUIInitialState import LUIInitialState

class LUIFrame(LUIObject):

    # Frame styles
    Sunken = 1
    Raised = 2

    """ A container which can store multiple ui-elements """

    def __init__(self, inner_padding=5, scrollable=False, style=Raised, **kwargs):
        """ Creates a new frame with the given options and style. If scrollable
        is True, the contents of the frame will scroll if they don't fit into
        the frame height. inner_padding only has effect if scrollable is True.
        You can call fit_to_children() to make the frame fit automatically to
        it's contents."""
        LUIObject.__init__(self)

        # Each *style* has a different border size (size of the shadow). The
        # border size shouldn't get calculated to the actual framesize, so we
        # are determining it first and then substracting it.
        # TODO: We could do this automatically, determined by the sprite size
        # probably?
        self._border_size = 0
        self.padding = 10
        self.solid = True
        prefix = ""

        if style == LUIFrame.Raised:
            self._border_size = 33
            prefix = "Frame_"
        elif style == LUIFrame.Sunken:
            self._border_size = 5
            prefix = "SunkenFrame_"
        else:
            print("LUIFrame: Unkown UIFrame style:", style)

        self._layout = LUICornerLayout(parent=self, image_prefix=prefix)
        LUIInitialState.init(self, kwargs)

        self._effective_padding = self.padding_top + self._border_size
        self._scrollable = scrollable
        self._layout.margin = -self._effective_padding

        # TODO: Scrollable
        # if self._scrollable:
        self.content = LUIObject(self)
            # self.content.size = (width, height)
            # self.content.pos = (self._border_size, self._border_size)
            # self.scrollContent = UIScrollableRegion(self.content, width=width-2*padding, height=height-2*padding, padding=inner_padding)
            # self.contentNode = self.scrollContent.get_content_node()

    def on_resized(self, event):
        """ Internal callback when the Frame got resized """
        self._layout.size = self.size + 2* self._border_size
        self._layout.update_layout()

    def fit_to_children(self):
        """ Resizes the frame so it exactly fits its contents """
        self._layout.size = 0, 0
        LUIObject.fit_to_children(self)

    def fit_height_to_children(self):
        """ Resizes the frame vertically to fit its contents """
        self._layout.size = 0, 0
        LUIObject.fit_height_to_children(self)

    def fit_width_to_children(self):
        """ Resizes the frame horizontally to fit its contents """
        self._layout.size = 0, 0
        LUIObject.fit_width_to_children(self)

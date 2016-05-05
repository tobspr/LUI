
from __future__ import print_function

from LUIObject import LUIObject
from LUISprite import LUISprite
from LUILayouts import LUICornerLayout
from LUIInitialState import LUIInitialState
from LUIScrollableRegion import LUIScrollableRegion

__all__ = ["LUIFrame"]


class LUIFrame(LUIObject):

    """ A container which can store multiple ui-elements. If you don't want a
    border/background, you should use an empty LUIObject as container instead.
    """

    FS_sunken = 1
    FS_raised = 2

    def __init__(self, inner_padding=5, scrollable=False, style=FS_raised,
                 **kwargs):
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

        if style == LUIFrame.FS_raised:
            temp = LUISprite(self, "Frame_Left", "skin")
            self._border_size = temp.width
            self.remove_child(temp)
            prefix = "Frame_"
        elif style == LUIFrame.FS_sunken:
            self._border_size = 0
            prefix = "SunkenFrame_"
        else:
            raise Exception("Unkown LUIFrame style: " + style)

        self._scrollable = scrollable
        self._layout = LUICornerLayout(parent=self, image_prefix=prefix)
        self._layout.margin = -(self.padding.top + self._border_size)
        if self._scrollable:
            self._content = LUIObject(self)
            self._content.size = (self.width, self.height)
            self._content.pos = (self._border_size, self._border_size)
            self._scroll_content = LUIScrollableRegion(
                self._content,
                width=self.width - 2 * self.padding.left,
                height=self.height - 2 * self.padding.left,
                padding=inner_padding)
            self.content_node = self._scroll_content.content_node

        LUIInitialState.init(self, kwargs)

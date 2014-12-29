

from panda3d.lui import LUIObject
from UILayouts import UICornerLayout


class UIFrame(UICornerLayout):

    Sunken = 1
    Default = 2

    def __init__(self, parent=None, width=None, height=200, padding=10, innerPadding=5, scrollable=False, style=Default):
        self.borderSize = 0

        if width is None:
            width = 100
            if parent is not None:
                width = parent.width - parent.padding_left - parent.padding_right

        prefix = ""

        if style == UIFrame.Default:
            self.borderSize = 33
            prefix = "Frame_"
        elif style == UIFrame.Sunken:
            self.borderSize = 5
            prefix = "SunkenFrame_"

        UICornerLayout.__init__(self, parent=parent, image_prefix=prefix, width=width+2*self.borderSize, height=height+2*self.borderSize)

        self.effectivePadding = padding + self.borderSize

        self.scrollable = scrollable
        self.content = LUIObject(self)
        # self.content.size = (width, height)
        # self.content.pos = (self.borderSize, self.borderSize)
        self.padding = (self.effectivePadding,self.effectivePadding,self.effectivePadding,self.effectivePadding)
        self.margin = (-self.borderSize, -self.borderSize, -self.borderSize, -self.borderSize)
        self.layoutContainer.margin = (-self.effectivePadding, -self.effectivePadding, -self.effectivePadding, -self.effectivePadding)
        self.contentNode = self.content

        # if self.scrollable:
            # self.scrollContent = UIScrollableRegion(self.content, width=width-2*padding, height=height-2*padding, padding=innerPadding)
            # self.contentNode = self.scrollContent.get_content_node()


    def fit_to_children(self):
        print "Hello!"
        self.layoutContainer.height = 0
        self.layoutContainer.width = 0
        UICornerLayout.fit_to_children(self)
        # Add padding
        self.width += self.effectivePadding
        self.height += self.effectivePadding
        self.update_layout()

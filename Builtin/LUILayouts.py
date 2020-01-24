
from __future__ import print_function, division

from LUIObject import LUIObject
from LUISprite import LUISprite
from LUIHorizontalLayout import LUIHorizontalLayout

from LUIInitialState import LUIInitialState

__all__ = ["LUICornerLayout", "LUIHorizontalStretchedLayout"]

class LUICornerLayout(LUIObject):

    """ This is a layout which is used to combine 9 sprites to a single sprite,
    e.g. used for box shadow or frames."""

    # List of all sprite identifiers required for the layout
    _MODES = ["TR", "Top", "TL", "Right", "Mid", "Left", "BR", "Bottom", "BL"]

    def __init__(self, image_prefix="", **kwargs):
        """ Creates a new layout, using the image_prefix as prefix. """
        LUIObject.__init__(self)
        self.set_size("100%", "100%")
        self._prefix = image_prefix
        self._parts = {}
        for i in self._MODES:
            self._parts[i] = LUISprite(self, "blank", "skin")
        self._update_layout()
        LUIInitialState.init(self, kwargs)

    def _update_layout(self):
        """ Updates the layouts components. """
        for i in self._MODES:
            self._parts[i].set_texture(self._prefix + i, "skin", resize=True)

        # Top and Left
        self._parts["Top"].width = "100%"
        self._parts["Top"].margin = (0, self._parts["TR"].width, 0, self._parts["TL"].width)

        self._parts["Left"].height = "100%"
        self._parts["Left"].margin = (self._parts["TL"].height, 0, self._parts["BL"].height, 0)

        # Mid
        self._parts["Mid"].set_size("100%", "100%")
        self._parts["Mid"].margin = (self._parts["Top"].height, self._parts["Right"].width,
                                     self._parts["Bottom"].height, self._parts["Left"].width)

        # Bottom and Right
        self._parts["Bottom"].width = "100%"
        self._parts["Bottom"].margin = (0, self._parts["BR"].width, 0, self._parts["BL"].width)
        self._parts["Bottom"].bottom = 0

        self._parts["Right"].height = "100%"
        self._parts["Right"].margin = (self._parts["TR"].height, 0, self._parts["BR"].width, 0)
        self._parts["Right"].right = 0

        # Corners
        self._parts["TL"].top_left = 0, 0
        self._parts["TR"].top_right = 0, 0
        self._parts["BL"].bottom_left = 0, 0
        self._parts["BR"].bottom_right = 0, 0

    def set_prefix(self, prefix):
        """ Changes the texture of the layout """
        self._prefix = prefix
        self._update_layout()

    def get_prefix(self):
        """ Returns the layouts texture prefix """
        return self._prefix

    prefix = property(get_prefix, set_prefix)


class LUIHorizontalStretchedLayout(LUIObject):

    """ A layout which takes 3 sprites, a left sprite, a right sprite, and a
    middle sprite. While the left and right sprites remain untouched, the middle
    one will be stretched to fit the layout """

    def __init__(self, parent=None, prefix="ButtonDefault", **kwargs):
        LUIObject.__init__(self)
        self._layout = LUIHorizontalLayout(self, spacing=0)
        self._layout.width = "100%"
        self._sprite_left = LUISprite(self._layout.cell(), "blank", "skin")
        self._sprite_mid = LUISprite(self._layout.cell('*'), "blank", "skin")
        self._sprite_right = LUISprite(self._layout.cell(), "blank", "skin")
        if parent is not None:
            self.parent = parent
        self.prefix = prefix
        LUIInitialState.init(self, kwargs)

    def set_prefix(self, prefix):
        """ Sets the layout prefix, this controls which sprites will be used """
        self._sprite_left.set_texture(prefix + "_Left", "skin")
        self._sprite_mid.set_texture(prefix, "skin")
        self._sprite_right.set_texture(prefix + "_Right", "skin")
        self._sprite_mid.width = "100%"
        self._prefix = prefix

    def get_prefix(self):
        """ Returns the layout prefix """
        return self._prefix

    prefix = property(get_prefix, set_prefix)

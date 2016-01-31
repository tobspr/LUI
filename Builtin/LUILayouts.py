
from __future__ import print_function, division

from panda3d.lui import *
from direct.directnotify.DirectNotify import DirectNotify

from LUIInitialState import LUIInitialState

__all__ = ["LUIBaseLayout", "LUIVerticalLayout", "LUIHorizontalLayout",
           "LUICornerLayout", "LUIHorizontalStretchedLayout"]

class LUIBaseLayout(LUIObject):

    """ Abstract class to supply a consistent interface for different layouts """

    def __init__(self, x, y, w, h, **kwargs):
        LUIObject.__init__(self, x, y, w, h)

    def add(self, *objects):
        """ Use to add elements """
        raise NotImplementedError()

    def remove(self, index):
        """ Use to delete cells """
        raise NotImplementedError()

    def reset(self):
        """ Resets the layout, removing all components """
        raise NotImplementedError()

    def get(self, index):
        """ Use to get an element """
        raise NotImplementedError()

class LUIVerticalLayout(LUIBaseLayout):

    """ A vertical layout storing components row-wise """

    def __init__(self, parent=None, spacing=2, use_dividers=False, **kwargs):
        """ Constructs a new layout with a given parent and with. spacing controls
        the distance between cells. If use_dividers is set to True, there will
        be horizontal lines between the cells """
        LUIBaseLayout.__init__(self, x=0, y=0, w=0, h=0)
        self._rows = []
        self._dividers = LUIObject(self, x=0, y=0, w=0, h=0)
        self._spacing = spacing
        self._use_dividers = use_dividers
        self._in_update_section = False
        if parent is not None:
            self.parent = parent
        LUIInitialState.init(self, kwargs)

    def reset(self):
        """ Resets the layout, removing all children and rows """
        self._rows = []
        self.remove_all_children()
        self.update()

    def get(self, index):
        """ Returns the n-th row element """
        return self._rows[index]

    def set_spacing(self, spacing):
        """ Sets the spacing between the rows in pixels """
        self._spacing = spacing
        self.update()

    def get_spacing(self):
        """ Returns the spacing between the rows in pixels """
        return self._spacing

    spacing = property(get_spacing, set_spacing)

    def add(self, *objects):
        """ Adds a new row containing all given objects """
        container = LUIObject(self, 0, 0, w=self.width, h=0)
        container.bind("child_changed", self._layout_changed)
        self._rows.append(container)
        for obj in objects:
            obj.parent = container
        self.update()

    def remove(self, index):
        """ Not implemented yet """
        raise NotImplementedError()

    def _add_divider(self, y_pos):
        """ Internal method to add a horizontal divider """
        if self._use_dividers:
            divider = LUISprite(self._dividers, "ListDivider", "skin")
            divider.width = self.width
            divider.top = y_pos - divider.height // 2

    def update(self):
        """ Updates the layout, recalculating all boxes """
        current_height = 0
        self._in_update_section = True
        self._dividers.remove_all_children()

        if self._use_dividers:
            current_height += self._spacing // 2

        for index, row in enumerate(self._rows):
            # row.fit_to_children()
            row.top = current_height
            current_height += row.height + self._spacing
            if index != len(self._rows) - 1:
                self._add_divider(current_height - self._spacing // 2)

        # self.fit_to_children()
        self._in_update_section = False

    def _layout_changed(self, event):
        """ Internal method when any object of the child layout got changed """
        if not self._in_update_section:
            self.update()

class LUIHorizontalLayout(LUIBaseLayout):

    """ Standard horizontal layout,
    objects are set next to each other from left to right """

    def __init__(self, parent=None, spacing=2, use_dividers=False, **kwargs):
        """ Constructs a new horizontal layout with a given height and parent.
        spacing controls the distance between cells. If use_dividers is set to
        True, there will be horizontal lines between the cells"""
        LUIBaseLayout.__init__(self, x=0, y=0, w=0, h=0)
        self._columns = []
        self._dividers = LUIObject(self, x=0, y=0, h=0, w=0)
        self._spacing = spacing
        self._use_dividers = use_dividers
        self._in_update_section = False
        if parent is not None:
            self.parent = parent
        LUIInitialState.init(self, kwargs)

    def reset(self):
        """ Resets the layout """
        self._columns = []
        self.remove_all_children()
        self.update()

    def set_spacing(self, spacing):
        """ Sets the spacing between the cells in pixels """
        self._spacing = spacing
        self.update()

    def get_spacing(self):
        """ Returns the spacing between the cells in pixels """
        return self._spacing

    spacing = property(get_spacing, set_spacing)

    def add(self, *objects):
        """ Adds a new column with the given objects """
        container = LUIObject(self, 0, 0, w=0, h=0)
        self._columns.append(container)
        container.bind("child_changed", self._layout_changed)
        for obj in objects:
            obj.parent = container
        self.update()

    def remove(self, index):
        """ Not implemented yet"""
        raise NotImplementedError()

    def _add_divider(self, x_pos):
        """ Internal method to add a new divider """
        if self._use_dividers:
            divider = LUISprite(self._dividers, "HorizontalListDivider", "skin")
            divider.height = self.height
            divider.left = x_pos - 1

    def update(self):
        """ Updates the layout, adjusting the size of all cells """
        current_x = 0
        self._in_update_section = True
        self._dividers.remove_all_children()

        if self._use_dividers:
            current_x += self._spacing // 2

        for index, column in enumerate(self._columns):
            # column.fit_to_children()
            column.left = current_x
            current_x += column.width + self._spacing
            if index != len(self._columns) - 1:
                self._add_divider(current_x - self._spacing // 2)

        # self.fit_to_children()
        self._in_update_section = False

    def get(self, index):
        """ Returns the n-th column object """
        if index >= 0 and index < len(self._columns):
            return self._columns[index]
        return None

    def _layout_changed(self, event):
        """ Internal method when any object of the child layout got changed """
        if not self._in_update_section:
            self.update()

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

    def __init__(self, parent=None, width=200, prefix="ButtonDefault"):
        LUIObject.__init__(self, x=0, y=0, w=width, h=-1)
        self._sprite_left = LUISprite(self, "blank", "skin")
        self._sprite_mid = LUISprite(self, "blank", "skin")
        self._sprite_right = LUISprite(self, "blank", "skin")
        self.width = "100%"
        self._sprite_right.right = 0
        self._sprite_mid.left = 0

        if parent is not None:
            self.parent = parent

        self.prefix = prefix

    def set_prefix(self, prefix):
        """ Sets the layout prefix, this controls which sprites will be used """
        self._sprite_left.set_texture(prefix + "_Left", "skin")
        self._sprite_mid.set_texture(prefix, "skin")
        self._sprite_right.set_texture(prefix + "_Right", "skin")
        self._sprite_mid.margin = (0, self._sprite_right.width, 0, self._sprite_left.width)
        self._sprite_mid.width = "100%"
        self._prefix = prefix

    def get_prefix(self):
        """ Returns the layout prefix """
        return self._prefix

    prefix = property(get_prefix, set_prefix)


from __future__ import print_function, division

from panda3d.lui import *
from direct.directnotify.DirectNotify import DirectNotify

from LUIInitialState import LUIInitialState

__all__ = ["LUIBaseLayout", "LUIVerticalLayout", "LUIHorizontalLayout",
           "LUICornerLayout", "LUIHorizontalStretchedLayout"]

class LUIBaseLayout(LUIObject):

    """ Abstract class to supply a consistent interface for different layouts """

    def __init__(self, x, y, w, h):
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

    def __init__(self, parent=None, width=None, spacing=2, use_dividers=False):
        """ Constructs a new layout with a given parent and with. spacing controls
        the distance between cells. If use_dividers is set to True, there will
        be horizontal lines between the cells """
        if width is None:
            width = 100
            if parent is not None:
                width = parent.width - parent.padding_left - parent.padding_right

        LUIBaseLayout.__init__(self, x=0, y=0, w=width, h=0)

        self._rows = []
        self._dividers = LUIObject(self, x=0, y=0, w=width, h=0)
        self._spacing = spacing
        self._use_dividers = use_dividers
        self._in_update_section = False
        if parent is not None:
            self.parent = parent

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
            row.fit_to_children()
            row.top = current_height
            current_height += row.height + self._spacing
            if index != len(self._rows) - 1:
                self._add_divider(current_height - self._spacing // 2)

        self.height = current_height
        self._in_update_section = False

    def _layout_changed(self, event):
        """ Internal method when any object of the child layout got changed """
        if not self._in_update_section:
            self.update()

class LUIHorizontalLayout(LUIBaseLayout):

    """ Standard horizontal layout,
    objects are set next to each other from left to right """

    def __init__(self, parent=None, height=None, spacing=2, use_dividers=False):
        """ Constructs a new horizontal layout with a given height and parent.
        spacing controls the distance between cells. If use_dividers is set to
        True, there will be horizontal lines between the cells"""
        if height is None:
            height = 100
            if parent is not None:
                height = parent.height - parent.padding_top - parent.padding_bottom

        LUIBaseLayout.__init__(self, x=0, y=0, w=0, h=height)

        self._columns = []
        self._dividers = LUIObject(self, x=0, y=0, h=height, w=0)
        self._spacing = spacing
        self._use_dividers = use_dividers
        self._in_update_section = False

        if parent is not None:
            self.parent = parent

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
        container = LUIObject(self, 0, 0, w=self.height, h=0)
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
            divider = LUISprite(self._dividers, "ListDivider", "skin")
            divider.height = self.height
            divider.left = x_pos

    def update(self):
        """ Updates the layout, adjusting the size of all cells """
        current_x = 0
        self._in_update_section = True
        self._dividers.remove_all_children()
        self._add_divider(0)

        if self._use_dividers:
            current_x += self._spacing // 2

        for column in self._columns:
            column.fit_to_children()
            column.left = current_x
            current_x += column.width + self._spacing
            self._add_divider(current_x - self._spacing // 2)

        self.width = current_x

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
        LUIObject.__init__(self, x=0, y=0, w=100, h=100)
        LUIInitialState.init(self, kwargs)
        self._prefix = image_prefix
        self._parts = {}
        for i in self._MODES:
            self._parts[i] = LUISprite(self, "blank", "skin")
        self.update_layout()

    def update_layout(self):
        """ Updates the layouts components. Should be called whenver the layout
        got resized """
        for i in self._MODES:
            self._parts[i].set_texture(self._prefix + i, "skin", resize=True)

        # Width
        self._parts['Top'].width = self.width - self._parts['TL'].width - self._parts['TR'].width
        self._parts['Mid'].width = self.width - self._parts['Left'].width - self._parts['Right'].width
        self._parts['Bottom'].width = self.width - self._parts['BL'].width - self._parts['BR'].width

        # Height
        self._parts['Left'].height = self.height - self._parts['TL'].height - self._parts['BL'].height
        self._parts['Mid'].height = self.height - self._parts['Top'].height - self._parts['Bottom'].height
        self._parts['Right'].height = self.height - self._parts['TR'].height - self._parts['BR'].height

        # Positioning - Left
        self._parts['Top'].left = self._parts['TL'].width
        self._parts['Mid'].left = self._parts['Left'].width
        self._parts['Bottom'].left = self._parts['BL'].width

        self._parts['TR'].left = self._parts['Top'].left + self._parts['Top'].width
        self._parts['Right'].left = self._parts['Mid'].left + self._parts['Mid'].width
        self._parts['BR'].left = self._parts['Bottom'].left + self._parts['Bottom'].width

        # Positioning - Top
        self._parts['Left'].top = self._parts['TL'].height
        self._parts['Mid'].top = self._parts['Top'].height
        self._parts['Right'].top = self._parts['TR'].height

        self._parts['BL'].top = self._parts['Left'].top + self._parts['Left'].height
        self._parts['Bottom'].top = self._parts['Mid'].top + self._parts['Mid'].height
        self._parts['BR'].top = self._parts['Right'].top + self._parts['Right'].height

    def set_prefix(self, prefix):
        """ Changes the texture of the layout """
        self._prefix = prefix
        self.update_layout()

    def get_prefix(self):
        """ Returns the layouts texture prefix """
        return self._prefix

    prefix = property(get_prefix, set_prefix)


class LUIHorizontalStretchedLayout(LUIObject):

    """ A layout which takes 3 sprites, a left sprite, a right sprite, and a
    middle sprite. While the left and right sprites remain untouched, the middle
    one will be stretched to fit the layout """

    def __init__(self, parent=None, width=200, prefix="ButtonDefault"):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        self._sprite_left = LUISprite(self, "blank", "skin")
        self._sprite_mid = LUISprite(self, "blank", "skin")
        self._sprite_right = LUISprite(self, "blank", "skin")
        self.prefix = prefix
        self.recompute()
        self.fit_to_children()

        if parent is not None:
            self.parent = parent

    def recompute(self):
        """ Recomputes the layout to fit new dimensions """
        self._sprite_mid.left = self._sprite_left.width
        self._sprite_mid.width = self.width - self._sprite_left.width - self._sprite_right.width
        self._sprite_right.left = self._sprite_mid.left + self._sprite_mid.width

    def set_prefix(self, prefix):
        """ Sets the layout prefix, this controls which sprites will be used """
        self._sprite_left.set_texture(prefix + "_Left", "skin")
        self._sprite_mid.set_texture(prefix, "skin")
        self._sprite_right.set_texture(prefix + "_Right", "skin")
        self._prefix = prefix
        self.recompute()

    def get_prefix(self):
        """ Returns the layout prefix """
        return self._prefix

    prefix = property(get_prefix, set_prefix)

    def get_sprite_left(self):
        """ Returns a handle to the left sprite, usually not required """
        return self._sprite_left

    def get_sprite_mid(self):
        """ Returns a handle to the middle sprite, usually not required """
        return self._sprite_mid

    def get_sprite_right(self):
        """ Returns a handle to the right sprite, usually not required """
        return self._sprite_right

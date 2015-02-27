from panda3d.lui import *
from direct.directnotify.DirectNotify import DirectNotify

from LUIInitialState import LUIInitialState

class LUILayout(LUIObject):

    """ Abstract class to supply consistent interface for different
    LUILayouts """

    def __init__(self, x, y, w, h):
        LUIObject.__init__(self, x, y, w, h)
        self.notify = DirectNotify().newCategory("LUI")

    """ Use to add elements """
    def add(self, *objects):
        notify.warning("LUILayout's base add method called, but it should be overriden!")
        return False

    """ Use to delete element """
    def remove(self, index):
        notify.warning("LUILayout's base remove method called, but it should be overriden!")
        return False

    """ Use to get an element """
    def get(self, index):
        notify.warning("LUILayout's base get method called, but it should be overriden!")
        return False


class LUIVerticalLayout(LUILayout):

    def __init__(self, parent=None, width=None, spacing=2, use_dividers=False):
        if width is None:
            width = 100
            if parent is not None:
                width = parent.width - parent.padding_left - parent.padding_right

        LUILayout.__init__(self, x=0, y=0, w=width, h=0)

        self.rows = []
        self.dividers = LUIObject(self, x=0, y=0, w=width, h=0)
        self.spacing = spacing
        self.useDividers = use_dividers

        if parent is not None:
            self.parent = parent

    def reset(self):
        self.rows = []
        self.remove_all_children()
        self.update()

    def set_spacing(self, spacing):
        self.spacing = spacing
        self.update()

    def add(self, *objects):
        self.add_row(*objects)

    def add_row(self, *objects):
        container = LUIObject(self, 0, 0, w=self.width, h=0)
        self.rows.append(container)

        for obj in objects:
            obj.parent = container
        self.update()

    """ Not implemented """
    def remove(self, *objects):
        pass

    def _add_divider(self, y_pos):
        if self.useDividers:
            divider = LUISprite(self.dividers, "ListDivider", "skin")
            divider.width = self.width
            divider.top = y_pos

    def update(self):
        currentY = 0

        self.dividers.remove_all_children()
        self._add_divider(0)

        if self.useDividers:
            currentY += self.spacing / 2

        for row in self.rows:
            row.fit_to_children()
            row.top = currentY
            currentY += row.get_height() + self.spacing
            self._add_divider(currentY - self.spacing / 2)

        self.height = currentY

    def get(self, index):
        return self.get_row(index)

    def get_row(self, index):
        if index >= 0 and index < len(self.rows):
            return self.rows[index]
        return None


class LUIHorizontalLayout(LUILayout):

    """ Standard horizontal layout,
    objects are set next to each other from left to right """

    def __init__(self, parent=None, height=None, spacing=2, use_dividers=False):
        if height is None:
            height = 100
            if parent is not None:
                height = parent.height - parent.padding_top - parent.padding_bottom

        LUILayout.__init__(self, x=0, y=0, w=0, h=height)

        self.columns = []
        self.dividers = LUIObject(self, x=0, y=0, h=height, w=0)
        self.spacing = spacing
        self.useDividers = use_dividers

        if parent is not None:
            self.parent = parent

    def reset(self):
        self.columns = []
        self.remove_all_children()
        self.update()

    def set_spacing(self, spacing):
        self.spacing = spacing
        self.update()

    def add(self, *objects):
        self.add_column(*objects)

    def add_column(self, *objects):
        container = LUIObject(self, 0, 0, w=self.height, h=0)
        self.columns.append(container)

        for obj in objects:
            obj.parent = container
        self.update()

    """ Not implemented """
    def remove(self, index):
        pass

    def _add_divider(self, x_pos):
        if self.useDividers:
            divider = LUISprite(self.dividers, "ListDivider", "skin")
            divider.height = self.height
            divider.left = x_pos

    def update(self):
        currentX = 0

        self.dividers.remove_all_children()
        self._add_divider(0)

        if self.useDividers:
            currentX += self.spacing / 2

        for column in self.columns:
            column.fit_to_children()
            column.left = currentX
            currentX += column.get_width() + self.spacing
            self._add_divider(currentX - self.spacing / 2)

        self.width = currentX

    def get(self, index):
        return self.get_column(index)

    def get_column(self, index):
        if index >= 0 and index < len(self.columns):
            return self.columns[index]
        return None

class LUICornerLayout(LUIObject):

    """ This is a layout which is used to combine 9 sprites to a single sprite,
    e.g. used for box shadow """

    modes = ["TR", "Top", "TL", "Right", "Mid", "Left", "BR", "Bottom", "BL"]

    def __init__(self, image_prefix="", **kwargs):
        """ Creates a new layout, using the image_prefix as prefix. """
        LUIObject.__init__(self, x=0, y=0, w=100, h=100)
        LUIInitialState.init(self, kwargs)
        self.prefix = image_prefix
        self.parts = {}
        for i in self.modes:
            self.parts[i] = LUISprite(self, "blank", "skin")
        self.update_layout()

    def update_layout(self):
        """ Updates the layouts components. Should be called whenver the layout
        got resized """
        for i in self.modes:
            self.parts[i].set_texture(self.prefix + i, "skin", resize=True)

        # Width
        self.parts['Top'].width = self.width - self.parts['TL'].width - self.parts['TR'].width
        self.parts['Mid'].width = self.width - self.parts['Left'].width - self.parts['Right'].width
        self.parts['Bottom'].width = self.width - self.parts['BL'].width - self.parts['BR'].width

        # Height
        self.parts['Left'].height = self.height - self.parts['TL'].height - self.parts['BL'].height
        self.parts['Mid'].height = self.height - self.parts['Top'].height - self.parts['Bottom'].height
        self.parts['Right'].height = self.height - self.parts['TR'].height - self.parts['BR'].height

        # Positioning - Left
        self.parts['Top'].left = self.parts['TL'].width
        self.parts['Mid'].left = self.parts['Left'].width
        self.parts['Bottom'].left = self.parts['BL'].width

        self.parts['TR'].left = self.parts['Top'].left + self.parts['Top'].width
        self.parts['Right'].left = self.parts['Mid'].left + self.parts['Mid'].width
        self.parts['BR'].left = self.parts['Bottom'].left + self.parts['Bottom'].width

        # Positioning - Top
        self.parts['Left'].top = self.parts['TL'].height
        self.parts['Mid'].top = self.parts['Top'].height
        self.parts['Right'].top = self.parts['TR'].height

        self.parts['BL'].top = self.parts['Left'].top + self.parts['Left'].height
        self.parts['Bottom'].top = self.parts['Mid'].top + self.parts['Mid'].height
        self.parts['BR'].top = self.parts['Right'].top + self.parts['Right'].height

    def set_prefix(self, prefix):
        """ Changes the texture of the layout """
        self.prefix = prefix
        self.update_layout()


class LUIHorizontalStretchedLayout(LUIObject):

    def __init__(self, parent=None, width=200, prefix="ButtonMagic"):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        self.spriteLeft = LUISprite(self, prefix + "_Left", "skin")
        self.spriteMid = LUISprite(self, prefix, "skin")
        self.spriteRight = LUISprite(self, prefix + "_Right", "skin")
        self.recompute()
        self.fit_to_children()

        if parent is not None:
            self.parent = parent

    def recompute(self):
        self.spriteMid.left = self.spriteLeft.width
        self.spriteMid.width = self.width - self.spriteLeft.width - self.spriteRight.width
        self.spriteRight.left = self.spriteMid.left + self.spriteMid.width

    def set_prefix(self, prefix):
        self.spriteLeft.set_texture(prefix + "_Left", "skin", resize=False)
        self.spriteMid.set_texture(prefix, "skin", resize=False)
        self.spriteRight.set_texture(prefix + "_Right", "skin", resize=False)

    def get_sprite_left(self):
        return self.spriteLeft

    def get_sprite_mid(self):
        return self.spriteMid

    def get_sprite_right(self):
        return self.spriteRight



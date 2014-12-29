

from panda3d.lui import *

class UIVerticalLayout(LUIObject):

    def __init__(self, parent=None, width=None, spacing=2, use_dividers=False):
        if width is None:
            width = 100
            if parent is not None:
                width = parent.width - parent.padding_left - parent.padding_right

        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        

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

    def add_row(self, *objects):
        container = LUIObject(self, 0, 0, w=self.width, h=0)
        self.rows.append(container)

        for obj in objects:
            obj.parent = container
        self.update()

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

    def get_row(self, index):
        if index >= 0 and index < len(self.rows):
            return self.rows[index]
        return None


class UICornerLayout(LUIObject):

    modes = ["TR", "Top", "TL", "Right", "Mid", "Left", "BR", "Bottom", "BL"]

    def __init__(self, parent=None, image_prefix="", width=0, height=0):
        LUIObject.__init__(self, x=0, y=0, w=width, h=height)

        self.prefix = image_prefix
        self.layoutContainer = LUIObject(self, x=0, y=0, w=width, h=height)
        self.parts = {}
        for i in self.modes:
            self.parts[i] = LUISprite(self.layoutContainer, "blank", "skin")
        self.update_layout()

        if parent is not None:
            self.parent = parent

    def update_layout(self):
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
        self.prefix = prefix
        self.update_layout()



class UIHorizontalStretchedLayout(LUIObject):

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
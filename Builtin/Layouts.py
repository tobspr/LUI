

from panda3d.lui import *

class UIVerticalLayout(LUIObject):

    def __init__(self, parent=None, width=200, spacing=2):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        self.rows = []
        self.spacing = spacing

        if parent is not None:
            self.parent = parent

    def reset(self):
        self.rows = []
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

    def update(self):
        currentY = 0
        for row in self.rows:
            row.fit_to_children()
            row.top = currentY
            currentY += row.get_height() + self.spacing

        self.height = currentY

    def get_row(self, index):
        if index >= 0 and index < len(self.rows):
            return self.rows[index]
        return None

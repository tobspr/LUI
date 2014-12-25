

from panda3d.lui import *

class UIVerticalLayout(LUIObject):

    def __init__(self, parent=None, width=200, spacing=2):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        self.columns = []
        self.spacing = spacing

        if parent is not None:
            self.parent = parent

    def set_spacing(self, spacing):
        self.spacing = spacing
        self.update()

    def add_column(self, *objects):
        container = LUIObject(self, 0, 0, w=self.width, h=0)
        self.columns.append(container)

        for obj in objects:
            obj.parent = container

        self.update()

    def update(self):
        currentY = 0
        for column in self.columns:
            column.fit_to_children()
            column.top = currentY
            currentY += column.get_height() + self.spacing

        self.height = currentY

    def get_column(self, index):
        if index >= 0 and index < len(self.columns):
            return self.columns[index]
        return None


from LUIObject import LUIObject

class LUIRadioboxGroup(LUIObject):

    """ Simple helper to group a bunch of LUIRadiobox and ensure only one is
    checked at one timem """

    def __init__(self):
        """ Constructs a new group without any radioboxes inside """
        self._boxes = []
        self._selected_box = None

    def register_box(self, box):
        """ Registers a box to the collection """
        if box not in self._boxes:
            self._boxes.append(box)

    def set_active_box(self, active_box):
        """ Internal function to set the active box """
        for box in self._boxes:
            if box is not active_box:
                box._update_state(False)
            else:
                box._update_state(True)
        self._selected_box = active_box

    def get_active_box(self):
        """ Returns the current selected box """
        return self._selected_box

    active_box = property(get_active_box, set_active_box)

    def get_active_value(self):
        """ Returns the value of the current selected box (or None if none is
        selected) """
        if self._selected_box is None:
            return None
        return self._selected_box.get_value()

    active_value = property(get_active_value)

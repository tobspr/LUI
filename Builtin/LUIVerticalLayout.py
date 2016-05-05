"""

This is a wrapper file. It contains no actual implementation

"""

from panda3d.lui import LUIVerticalLayout as _LUIVerticalLayout
from LUIInitialState import LUIInitialState

__all__ = ["LUIVerticalLayout"]


class LUIVerticalLayout(_LUIVerticalLayout):
    """ This is a wrapper class for the C++ LUIVerticalLayout class, to be
    able to use it in a more convenient way. It leverages LUIInitialState
    to be able to pass arbitrary keyword arguments. """

    def __init__(self, parent=None, spacing=0.0, **kwargs):
        _LUIVerticalLayout.__init__(self, parent, spacing)
        LUIInitialState.init(self, kwargs)

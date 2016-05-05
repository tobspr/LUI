"""

This is a wrapper file. It contains no actual implementation

"""

from panda3d.lui import LUIHorizontalLayout as _LUIHorizontalLayout
from LUIInitialState import LUIInitialState

__all__ = ["LUIHorizontalLayout"]


class LUIHorizontalLayout(_LUIHorizontalLayout):
    """ This is a wrapper class for the C++ LUIHorizontalLayout class, to be
    able to use it in a more convenient way. It leverages LUIInitialState
    to be able to pass arbitrary keyword arguments. """

    def __init__(self, parent=None, spacing=0.0, **kwargs):
        _LUIHorizontalLayout.__init__(self, parent, spacing)
        LUIInitialState.init(self, kwargs)

"""

This is a wrapper file. It contains no actual implementation

"""

from panda3d.lui import LUIObject as _LUIObject
from LUIInitialState import LUIInitialState

__all__ = ["LUIObject"]

class LUIObject(_LUIObject):
    """ This is a wrapper class for the C++ LUIObject class, to be able to
    use it in a more convenient way """

    def __init__(self, *args, **kwargs):
        _LUIObject.__init__(self, *args)
        LUIInitialState.init(self, kwargs)

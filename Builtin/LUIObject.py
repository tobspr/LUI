"""

This is a wrapper file. It contains no actual implementation

"""

from panda3d.lui import LUIObject as __LUIObject
from .LUIInitialState import LUIInitialState

__all__ = ["LUIObject"]

class LUIObject(__LUIObject):
    """ This is a wrapper class for the C++ LUIObject class, to be able to
    use it in a more convenient way """

    def __init__(self, x=0, y=0, w=-1, h=-1, solid=False, **kwargs):
        LUIObject.__init__(self, x, y, w, h, solid)
        LUIInitialState.init(self, kwargs)

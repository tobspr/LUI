"""

This is a wrapper file. It contains no actual implementation

"""

from panda3d.lui import LUISprite as _LUISprite
from LUIInitialState import LUIInitialState

__all__ = ["LUISprite"]

class LUISprite(_LUISprite):
    """ This is a wrapper class for the C++ LUISprite class, to be able to
    use it in a more convenient way """

    def __init__(self, *args, **kwargs):
        _LUISprite.__init__(self, *args)
        LUIInitialState.init(self, kwargs)

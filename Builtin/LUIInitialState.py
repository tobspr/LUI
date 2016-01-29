
__all__ = ["LUIFrame"]

class LUIInitialState:

    """ Small helper class to pass keyword arguments to the LUI-objects. It takes
    all keyword arguments of a given call, and calls obj.<kwarg> = <value>. """

    @staticmethod
    def init(obj, kwargs):
        """ Applies the keyword arguments as properties """
        for arg,val in kwargs.items():
            setattr(obj, arg, val)

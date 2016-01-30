
__all__ = ["LUIFrame"]

class LUIInitialState:

    """ Small helper class to pass keyword arguments to the LUI-objects. It takes
    all keyword arguments of a given call, and calls obj.<kwarg> = <value>. """

    @staticmethod
    def init(obj, kwargs):
        """ Applies the keyword arguments as properties """
        for arg_name, arg_val in kwargs.items():
            if hasattr(obj, arg_name):
                setattr(obj, arg_name, arg_val)
            else:
                raise AttributeError("{0} has no attribute {1}".format(
                    obj.__class__.__name__, arg_name))

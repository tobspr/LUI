
__all__ = ["LUIInitialState"]


class LUIInitialState:

    """ Small helper class to pass keyword arguments to the LUI-objects. It takes
    all keyword arguments of a given call, and calls obj.<kwarg> = <value> for
    each keyword. It usually is called at the end of the __init__ method. """

    def __init__(self):
        raise Exception("LUIInitialState is a static class")

    # Some properties have alternative names, under which they can be accessed.
    __MAPPINGS = {
        "x": "left",
        "y": "top",
        "w": "width",
        "h": "height"
    }

    @classmethod
    def init(cls, obj, kwargs):
        """ Applies all keyword arguments as properties. For example, passing
        dict({"left": 10, "top": 3, "color": (0.2, 0.6, 1.0)}) results in
        behaviour similar to:

            element.left = 10
            element.top = 3
            element.color = 0.2, 0.6, 1.0

        Calling this method allows setting arbitrary properties in
        constructors, without having to specify each possible keyword argument.
        """
        for arg_name, arg_val in kwargs.items():
            arg_name = cls.__MAPPINGS.get(arg_name, arg_name)
            if hasattr(obj, arg_name):
                setattr(obj, arg_name, arg_val)
            else:
                raise AttributeError("{0} has no attribute {1}".format(
                    obj.__class__.__name__, arg_name))

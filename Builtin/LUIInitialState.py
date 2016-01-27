
class LUIInitialState:

    """ Small helper class to pass keyword arguments to the LUI-objects """

    @staticmethod
    def init(obj, kwargs):
        """ Applies the keyword arguments as properties """
        for arg,val in kwargs.items():
            setattr(obj, arg, val)

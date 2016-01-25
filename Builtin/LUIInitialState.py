
class LUIInitialState:

    """ Small helper class to parse keyword arguments to the ui-objects """

    @staticmethod
    def init(obj, kwargs):
        """ Applies the keyword arguments as properties """
        for arg,val in kwargs.items():
            setattr(obj, arg, val)

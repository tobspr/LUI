

"""


OBSOLETE

Do not use anymore! Use trigger_event instead!


"""



class LUICallback:

    """ This class is used by the LUI Builtin objects to trigger a callback
    whenever their value changed (e.g. when an UICheckbox gets checked). The
    user may listen to this elements with add_change_callback. """

    def __init__(self):
        self._callbacks = []

    def add_change_callback(self, callback_function):
        """ Adds a new listener. The callback function will get called whenever
        this elements value gets modified, and recieve the element aswell as the
        value as parameters """
        if callback_function not in self._callbacks:
            self._callbacks.append(callback_function)

    def remove_change_callback(self, callback_function):
        """ Removes a callback which was set by add_change_callback """
        if callback_function in self._callbacks:
            self._callbacks.remove(callback_function)

    def forward_callbacks(self, obj):
        """ Listens to all events of the given object and when a callback is
        thrown, re-throws this callback on this instance """
        obj.add_change_callback(self._forward_cb)

    def _trigger_callback(self, *args, **kwargs):
        """ This is the internal function to trigger the change callback and
        will get called by the UI-Elements """
        for callback_function in self._callbacks:
            callback_function(self, *args, **kwargs)

    def _forward_cb(self, *args, **kwargs):
        """ This is an internal helper function to forward a callback """
        for callback_function in self._callbacks:
            callback_function(*args, **kwargs)

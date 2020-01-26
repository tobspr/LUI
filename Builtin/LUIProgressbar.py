
from LUIObject import LUIObject
from LUISprite import LUISprite

from LUILayouts import LUIHorizontalStretchedLayout
from LUILabel import LUILabel

class LUIProgressbar(LUIObject):

    """ A simple progress bar """

    def __init__(self, parent=None, width=200, value=50, show_label=True):
        """ Constructs a new progress bar. If show_label is True, a label indicating
        the current progress is shown """
        LUIObject.__init__(self)
        self.set_width(width)

        self._bg_layout = LUIHorizontalStretchedLayout(
            parent=self, prefix="ProgressbarBg", width="100%")

        self._fg_left = LUISprite(self, "ProgressbarFg_Left", "skin")
        self._fg_mid = LUISprite(self, "ProgressbarFg", "skin")
        self._fg_right = LUISprite(self, "ProgressbarFg_Right", "skin")
        self._fg_finish = LUISprite(self, "ProgressbarFg_Finish", "skin")

        self._show_label = show_label
        self._progress_pixel = 0
        self._fg_finish.right = 0

        if self._show_label:
            self._progress_label = LUILabel(parent=self, text=u"33 %")
            self._progress_label.centered = (True, True)

        self.set_value(value)
        self._update_progress()

        if parent is not None:
            self.parent = parent

    def get_value(self):
        """ Returns the current value of the progress bar """
        return (self._progress_pixel / self.width * 100.0)

    def set_value(self, val):
        """ Sets the value of the progress bar """
        val = max(0, min(100, val))
        self._progress_pixel = int(val / 100.0 * self.width)
        self._update_progress()

    value = property(get_value, set_value)

    def _update_progress(self):
        """ Internal method to update the progressbar """
        self._fg_finish.hide()

        if self._progress_pixel <= self._fg_left.width + self._fg_right.width:
            self._fg_mid.hide()
            self._fg_right.left = self._fg_left.width
        else:
            self._fg_mid.show()
            self._fg_mid.left = self._fg_left.width
            self._fg_mid.width = self._progress_pixel - self._fg_right.width - self._fg_left.width
            self._fg_right.left = self._fg_mid.left + self._fg_mid.width

            if self._progress_pixel >= self.width - self._fg_right.width:
                self._fg_finish.show()
                self._fg_finish.right = - (self.width - self._progress_pixel)
                self._fg_finish.clip_bounds = (0, self.width - self._progress_pixel, 0, 0)

        if self._show_label:
            percentage = self._progress_pixel / self.width * 100.0
            self._progress_label.set_text("{} %".format(int(percentage)))


from LUIObject import LUIObject
from LUISprite import LUISprite
from LUIInitialState import LUIInitialState
from LUILayouts import LUIHorizontalStretchedLayout

class LUISlider(LUIObject):

    """ Slider which can be used to control values """

    def __init__(self, parent=None, filled=True, min_value=0.0, max_value=1.0, width=100.0, value=None, **kwargs):
        """ Constructs a new slider. If filled is True, the part behind the knob
        will be solid """
        LUIObject.__init__(self, x=0, y=0, solid=True)
        self.set_width(width)
        self._knob = LUISprite(self, "SliderKnob", "skin")
        self._knob.z_offset = 2
        self._knob.solid = True

        # Construct the background
        self._slider_bg = LUIHorizontalStretchedLayout(parent=self, prefix="SliderBg", center_vertical=True, width="100%", margin=(-1, 0, 0, 0))

        self._filled = filled
        self._min_value = min_value
        self._max_value = max_value

        self._side_margin = self._knob.width / 4
        self._effective_width = self.width - 2 * self._side_margin

        if self._filled:
            self._slider_fill = LUIObject(self)
            self._fill_left = LUISprite(self._slider_fill, "SliderBgFill_Left", "skin")
            self._fill_mid = LUISprite(self._slider_fill, "SliderBgFill", "skin")
            self._fill_mid.left = self._fill_left.width
            self._slider_fill.z_offset = 1
            self._slider_fill.center_vertical = True

        if parent is not None:
            self.parent = parent

        # Handle various events
        self._knob.bind("mousedown", self._start_drag)
        self._knob.bind("mousemove", self._update_drag)
        self._knob.bind("mouseup", self._stop_drag)
        self._knob.bind("keydown", self._on_keydown)
        self._knob.bind("blur", self._stop_drag)
        self._knob.bind("keyrepeat", self._on_keydown)

        self._drag_start_pos = None
        self._dragging = False
        self._drag_start_val = 0
        self.current_val = 10

        # Set initial value
        if value is None:
            self.set_value( (self._min_value + self._max_value) / 2.0 )
        else:
            self.set_value(value)

        self._update_knob()

        LUIInitialState.init(self, kwargs)

    def on_click(self, event):
        """ Internal on click handler """
        # I don't like this behaviour
        # relative_pos = self.get_relative_pos(event.coordinates)
        # if not self._dragging:
        #     self._set_current_val(relative_pos.x)

    def _update_knob(self):
        """ Internal method to update the slider knob """
        self._knob.left = self.current_val - (self._knob.width / 2) + self._side_margin
        if self._filled:
            self._fill_mid.width = self.current_val - self._fill_left.width + self._side_margin

    def _set_current_val(self, pixels):
        """ Internal method to set the current value in pixels """
        pixels = max(0, min(self._effective_width, pixels))
        self.current_val = pixels
        self.trigger_event("changed")
        self._update_knob()

    def _start_drag(self, event):
        """ Internal drag start handler """
        self._knob.request_focus()
        if not self._dragging:
            self._drag_start_pos = event.coordinates
            self._dragging = True
            self._drag_start_val = self.current_val
            self._knob.color = (0.8,0.8,0.8,1.0)

    def set_value(self, value):
        """ Sets the value of the slider, should be between minimum and maximum. """
        scaled = (float(value) - float(self._min_value)) \
                 / (float(self._max_value) - float(self._min_value)) \
                 * self._effective_width
        self._set_current_val(scaled)

    def get_value(self):
        """ Returns the current value of the slider """
        return (self.current_val / float(self._effective_width)) \
                 * (float(self._max_value) - float(self._min_value)) \
                + self._min_value

    value = property(get_value, set_value)

    def _on_keydown(self, event):
        """ Internal keydown handler """
        if event.message == "arrow_right":
            self._set_current_val(self.current_val + 2)
        elif event.message == "arrow_left":
            self._set_current_val(self.current_val - 2)
        elif event.message == "escape":
            self.current_val = self._drag_start_val
            self._stop_drag(event)
            self._update_knob()

    def _update_drag(self, event):
        """ Internal drag handler """
        if self._dragging:
            dragOffset = event.coordinates.x - self._drag_start_pos.x
            finalValue = self._drag_start_val + dragOffset
            self._set_current_val(finalValue)

    def _stop_drag(self, event):
        """ Internal drag stop handelr """
        self._drag_start_pos = None
        self._dragging = False
        self._drag_start_val = self.current_val
        self._knob.color = (1,1,1,1)

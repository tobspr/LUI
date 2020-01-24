
from LUIObject import LUIObject
from LUISprite import LUISprite
from LUIInitialState import LUIInitialState
from LUILayouts import LUIHorizontalStretchedLayout

class LUIScrollableRegion(LUIObject):

    """ Scrollable region, reparent elements to the .content_node to make them
    scroll. """

    def __init__(self, parent=None, width=100, height=100, padding=10, **kwargs):
        LUIObject.__init__(self)
        self.set_size(width, height)
        self._content_parent = LUIObject(self)
        self._content_parent.set_size("100%", "100%")
        self._content_parent.clip_bounds = (0,0,0,0)

        self._content_clip = LUIObject(self._content_parent, x=padding, y=padding)
        self._content_clip.set_size("100%", "100%")

        self._content_scroller = LUIObject(self._content_clip)
        self._content_scroller.width = "100%"


        self._scrollbar = LUIObject(self, x=0, y=0, w=20)
        self._scrollbar.height = "100%"
        self._scrollbar.right = -10

        self._scrollbar_bg = LUISprite(self._scrollbar, "blank", "skin")
        self._scrollbar_bg.color = (1,1,1,0.05)
        self._scrollbar_bg.set_size(3, "100%")
        self._scrollbar_bg.center_horizontal = True

        # Handle
        self._scrollbar_handle = LUIObject(self._scrollbar, x=5, y=0, w=10)
        self._scroll_handle_top = LUISprite(self._scrollbar_handle, "ScrollbarHandle_Top", "skin")
        self._scroll_handle_mid = LUISprite(self._scrollbar_handle, "ScrollbarHandle", "skin")
        self._scroll_handle_bottom = LUISprite(self._scrollbar_handle, "ScrollbarHandle_Bottom", "skin")

        self._scrollbar_handle.solid = True
        self._scrollbar.solid = True

        self._scrollbar_handle.bind("mousedown", self._start_scrolling)
        self._scrollbar_handle.bind("mouseup", self._stop_scrolling)
        self._scrollbar.bind("mousedown", self._on_bar_click)
        self._scrollbar.bind("mouseup", self._stop_scrolling)

        self._handle_dragging = False
        self._drag_start_y = 0

        self._scroll_top_position = 0
        self._content_height = 400

        # Scroll shadow
        self._scroll_shadow_top = LUIHorizontalStretchedLayout(parent=self, prefix="ScrollShadowTop", width="100%")
        self._scroll_shadow_bottom = LUIHorizontalStretchedLayout(parent=self, prefix="ScrollShadowBottom", width="100%")
        self._scroll_shadow_bottom.bottom = 0

        self._handle_height = 100

        if parent is not None:
            self.parent = parent

        LUIInitialState.init(self, kwargs)
        self.content_node = self._content_scroller
        taskMgr.doMethodLater(0.05, lambda task: self._update(), "update_scrollbar")

    def _on_bar_click(self, event):
        """ Internal handler when the user clicks on the scroll bar """
        self._scroll_to_bar_pixels(event.coordinates.y - self._scrollbar.abs_pos.y - self._handle_height / 2.0)
        self._update()
        self._start_scrolling(event)

    def _start_scrolling(self, event):
        """ Internal method when we start scrolling """
        self.request_focus()
        if not self._handle_dragging:
            self._drag_start_y = event.coordinates.y
            self._handle_dragging = True

    def _stop_scrolling(self, event):
        """ Internal handler when we should stop scrolling """
        if self._handle_dragging:
            self._handle_dragging = False
            self.blur()

    def _scroll_to_bar_pixels(self, pixels):
        """ Internal method to convert from pixels to a relative position """
        offset = pixels * self._content_height / self.height
        self._scroll_top_position = offset
        self._scroll_top_position = max(0, min(self._content_height - self._content_clip.height, self._scroll_top_position))

    def on_tick(self, event):
        """ Internal on tick handler """
        if self._handle_dragging:
            scroll_abs_pos = self._scrollbar.abs_pos
            clamped_coord_y = max(scroll_abs_pos.y, min(scroll_abs_pos.y + self.height, event.coordinates.y))
            offset = clamped_coord_y - self._drag_start_y
            self._drag_start_y = clamped_coord_y
            self._scroll_to_bar_pixels(self._scroll_top_position/self._content_height*self.height + offset)
        self._update()

    def _set_handle_height(self, height):
        """ Internal method to set the scrollbar height """
        self._scroll_handle_mid.top = float(self._scroll_handle_top.height)

        self._scroll_handle_mid.height = max(0.0, height - self._scroll_handle_top.height - self._scroll_handle_bottom.height)
        self._scroll_handle_bottom.top = self._scroll_handle_mid.height + self._scroll_handle_mid.top
        self._handle_height = height

    def _update(self):
        """ Internal method to update the scroll bar """
        self._content_height = max(1, self._content_scroller.get_height() + 20)
        self._content_scroller.top = -self._scroll_top_position
        scrollbar_height = max(0.1, min(1.0, self._content_clip.height / self._content_height))
        scrollbar_height_px = scrollbar_height * self.height

        self._set_handle_height(scrollbar_height_px)
        self._scrollbar_handle.top = self._scroll_top_position / self._content_height * self.height

        top_alpha = max(0.0, min(1.0, self._scroll_top_position / 50.0))
        bottom_alpha = max(0.0, min(1.0, (self._content_height - self._scroll_top_position - self._content_clip.height) / 50.0 ))
        self._scroll_shadow_top.color = (1,1,1,top_alpha)
        self._scroll_shadow_bottom.color = (1,1,1,bottom_alpha)

        if self._content_height <= self.height:
            self._scrollbar_handle.hide()
        else:
            self._scrollbar_handle.show()

    def on_element_added(self):
        taskMgr.doMethodLater(0.05, lambda task: self._update(), "update_layout")

    def get_scroll_percentage(self):
        """ Returns the current scroll height in percentage from 0 to 1 """
        return self._scroll_top_position / max(1, self._content_height - self._content_clip.height)

    def set_scroll_percentage(self, percentage):
        """ Sets the scroll position in percentage, 0 means top and 1 means bottom """
        percentage = max(0.0, min(1.0, percentage))
        pixels =  max(0.0, self._content_height - self._content_clip.height) * percentage
        self._scroll_top_position = pixels
        self._update()

    scroll_percentage = property(get_scroll_percentage, set_scroll_percentage)

    def scroll_to_bottom(self):
        """ Scrolls to the bottom of the frame """
        taskMgr.doMethodLater(0.07, lambda task: self.set_scroll_percentage(1.0), "scroll_to_bottom")

    def scroll_to_top(self):
        """ Scrolls to the top of the frame """
        taskMgr.doMethodLater(0.07, lambda task: self.set_scroll_percentage(0.0), "scroll_to_top")


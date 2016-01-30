
from panda3d.lui import LUIObject, LUISprite
from LUIInitialState import LUIInitialState

class LUIScrollableRegion(LUIObject):

    """ Scrollable region """

    def __init__(self, parent, width=100, height=100, padding=10, **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=width, h=height)

        self._content_parent = LUIObject(self, x=0, y=0, w=width, h=height)
        self._content_parent.clip_bounds = (0,0,0,0)

        self.content_clip = LUIObject(self._content_parent, x=padding, y=padding, w=self.width - 2*padding, h=self.height - 2*padding)
        self.content_scroller = LUIObject(self.content_clip, x=0, y=0, w=self.content_clip.width, h=500)

        self._scrollbar = LUIObject(self, x=0, y=0, w=20, h=self.height)
        self._scrollbar.right = -10

        self._scrollbar_height = self.height
        self._scrollbar_bg = LUISprite(self._scrollbar, "blank", "skin")
        self._scrollbar_bg.color = (1,1,1,0.1)
        self._scrollbar_bg.size = (5, self._scrollbar_height)
        self._scrollbar_bg.left = 8

        # Handle
        self._scrollbar_handle = LUIObject(self._scrollbar, x=5, y=0, w=10, h=100)
        self._scroll_handle_top = LUISprite(self._scrollbar_handle, "ScrollbarHandle_Top", "skin")
        self._scroll_handle_mid = LUISprite(self._scrollbar_handle, "ScrollbarHandle", "skin")
        self._scroll_handle_bottom = LUISprite(self._scrollbar_handle, "ScrollbarHandle_Bottom", "skin")

        self._scrollbar_handle.solid = True
        self._scrollbar.solid = True

        self._scrollbar_handle.bind("mousedown", self._start_scrolling)
        self._scrollbar_handle.bind("mouseup", self._stop_scrolling)
        self._scrollbar.bind("mousedown", self._on_bar_click)
        self._scrollbar.bind("mouseup", self._stop_scrolling)

        self.content_scroller.bind("child_changed", self._update_height)

        self._handle_dragging = False
        self._drag_start_y = 0

        self._scroll_top_position = 0
        self._content_height = 400

        scroll_shadow_width = self.width - 10

        # Top shadow
        self._scroll_shadow_top = LUIObject(self)
        self._scroll_shadow_top_left = LUISprite(self._scroll_shadow_top, "ScrollShadow_BL", "skin")
        self._scroll_shadow_top_mid = LUISprite(self._scroll_shadow_top, "ScrollShadow_Bottom", "skin")
        self._scroll_shadow_top_right = LUISprite(self._scroll_shadow_top, "ScrollShadow_BR", "skin")
        self._scroll_shadow_top_mid.left = self._scroll_shadow_top_left.width
        self._scroll_shadow_top_mid.width = scroll_shadow_width - self._scroll_shadow_top_left.width - self._scroll_shadow_top_right.width
        self._scroll_shadow_top_right.left = self._scroll_shadow_top_mid.left + self._scroll_shadow_top_mid.width

        # Bottom shadow
        self._scroll_shadow_bottom = LUIObject(self)
        self._scroll_shadow_bottom_left = LUISprite(self._scroll_shadow_bottom, "ScrollShadow_TL", "skin")
        self._scroll_shadow_bottom_mid = LUISprite(self._scroll_shadow_bottom, "ScrollShadow_Top", "skin")
        self._scroll_shadow_bottom_right = LUISprite(self._scroll_shadow_bottom, "ScrollShadow_TR", "skin")
        self._scroll_shadow_bottom_mid.left = self._scroll_shadow_bottom_left.width
        self._scroll_shadow_bottom_mid.width = scroll_shadow_width - self._scroll_shadow_bottom_left.width - self._scroll_shadow_bottom_right.width
        self._scroll_shadow_bottom_right.left = self._scroll_shadow_bottom_mid.left + self._scroll_shadow_bottom_mid.width
        self._scroll_shadow_bottom.bottom = 0
        self._scroll_shadow_bottom_left.bottom = 0
        self._scroll_shadow_bottom_mid.bottom = 0
        self._scroll_shadow_bottom_right.bottom = 0

        self._handle_height = 100
        self._update()

        if parent is not None:
            self.parent = parent

        LUIInitialState.init(self, kwargs)

    def _on_bar_click(self, event):
        self._scroll_to_bar_pixels(event.coordinates.y - self._scrollbar.abs_pos.y - self._handle_height / 2.0)
        self._update()
        self._start_scrolling(event)

    def _start_scrolling(self, event):
        self.request_focus()
        if not self._handle_dragging:
            self._drag_start_y = event.coordinates.y
            self._handle_dragging = True

    def _update_height(self, event):
        self.content_scroller.fit_height_to_children()
        self._content_height = max(1, self.content_scroller.height)
        self._update()

    def _stop_scrolling(self, event):
        if self._handle_dragging:
            self._handle_dragging = False
            self.blur()

    def _scroll_to_bar_pixels(self, pixels):
        offset = pixels * self._content_height / self.height
        self._scroll_top_position = offset
        self._scroll_top_position = max(0, min(self._content_height - self.content_clip.height, self._scroll_top_position))

    def on_tick(self, event):
        if self._handle_dragging:
            scroll_abs_pos = self._scrollbar.abs_pos
            clamped_coord_y = max(scroll_abs_pos.y, min(scroll_abs_pos.y + self._scrollbar_height, event.coordinates.y))
            offset = clamped_coord_y - self._drag_start_y
            self._drag_start_y = clamped_coord_y
            self._scroll_to_bar_pixels(self._scroll_top_position/self._content_height*self.height + offset)
        self._update()

    def _set_handle_height(self, height):
        self._scroll_handle_mid.top = self._scroll_handle_top.height
        self._scroll_handle_mid.height = height - self._scroll_handle_top.height - self._scroll_handle_bottom.height
        self._scroll_handle_bottom.top = self._scroll_handle_mid.height + self._scroll_handle_mid.top
        self._handle_height = height

    def _update(self):
        self.content_scroller.top = -self._scroll_top_position
        scrollbar_height = max(0.1, min(1.0, self.content_clip.height / self._content_height))
        scrollbar_height_px = scrollbar_height * self.height
        self._set_handle_height(scrollbar_height_px)
        self._scrollbar_handle.top = self._scroll_top_position / self._content_height * self.height

        top_alpha = max(0.0, min(1.0, self._scroll_top_position / 50.0))
        bottom_alpha = max(0.0, min(1.0, (self._content_height - self._scroll_top_position - self.content_clip.height) / 50.0 ))
        self._scroll_shadow_top.color = (1,1,1,top_alpha)
        self._scroll_shadow_bottom.color = (1,1,1,bottom_alpha)


    def scroll_to_bottom(self):
        self._scroll_top_position = max(0, self._content_height - self.content_clip.height)
        self._update()

    def get_content_node(self):
        return self.content_scroller

    content_node = property(get_content_node)

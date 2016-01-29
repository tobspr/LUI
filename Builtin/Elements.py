from panda3d.lui import *
from panda3d.core import Point2

from functools import partial
from LUILayouts import *

import math
import colorsys

from LUICallback import LUICallback
from LUILabel import LUILabel
from LUIFrame import LUIFrame
from LUIButton import LUIButton

class LUISlider(LUIObject, LUICallback):

    def __init__(self, parent=None, filled=False, min_value=0.0, max_value=1.0, width=100.0, value=None):

        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        LUICallback.__init__(self)
        self.knob = LUISprite(self, "SliderKnob", "skin")
        self.knob.z_offset = 2

        self.sliderBg = LUIObject(self, 0, 0, width, 0)
        self.bgLeft = LUISprite(self.sliderBg, "SliderBg_Left", "skin")
        self.bgRight = LUISprite(self.sliderBg, "SliderBg_Right", "skin")
        self.bgMid = LUISprite(self.sliderBg, "SliderBg", "skin")

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.filled = filled
        self.min_value = min_value
        self.max_value = max_value

        self.sliderBg.fit_to_children()
        self.sliderBg.top = (self.knob.height - self.sliderBg.height) / 2 -1

        self.sideMargin = self.knob.width / 4
        self.effectiveWidth = self.width - 2 * self.sideMargin

        if self.filled:
            self.sliderFill = LUIObject(self, 0, 0, width, 0)
            self.fillLeft = LUISprite(self.sliderFill, "SliderBgFill_Left", "skin")
            self.fillMid = LUISprite(self.sliderFill, "SliderBgFill", "skin")
            self.fillMid.left = self.fillLeft.width
            self.sliderFill.z_offset = 1
            self.sliderFill.top = self.sliderBg.top
            self.sliderFill.fit_to_children()

        if parent is not None:
            self.parent = parent

        self.knob.bind("mousedown", self._start_drag)
        self.knob.bind("mousemove", self._update_drag)
        self.knob.bind("mouseup", self._stop_drag)
        self.knob.bind("keydown", self._on_keydown)
        self.knob.bind("blur", self._stop_drag)
        self.knob.bind("keyrepeat", self._on_keydown)


        self.dragStartPos = None
        self.dragging = False
        self.dragStartVal = 0
        self.currentVal = 10

        if value is None:
            self.set_value( (self.min_value + self.max_value) / 2.0 )
        else:
            self.set_value(value)

        self.fit_to_children()
        self._update_knob()

    def on_click(self, event):
        # I don't like this behaviour
        if False:
            relative_pos = self.get_relative_pos(event.coordinates)
            if not self.dragging:
                self._set_current_val(relative_pos.x)

    def _update_knob(self):
        self.knob.left = self.currentVal - (self.knob.width / 2) + self.sideMargin
        if self.filled:
            self.fillMid.width = self.currentVal - self.fillLeft.width + self.sideMargin

    def _set_current_val(self, pixels):
        pixels = max(0, min(self.effectiveWidth, pixels))
        self.currentVal = pixels
        self._trigger_callback(self.get_value())
        self._update_knob()

    def _start_drag(self, event):
        self.knob.request_focus()
        if not self.dragging:
            self.dragStartPos = event.coordinates
            self.dragging = True
            self.dragStartVal = self.currentVal
            self.knob.color = (0.8,0.8,0.8,1.0)

    def set_value(self, value):
        scaled = (float(value) - float(self.min_value)) \
                 / (float(self.max_value) - float(self.min_value)) \
                 * self.effectiveWidth
        self._set_current_val(scaled)


    def get_value(self):
        return (self.currentVal / float(self.effectiveWidth)) \
                 * (float(self.max_value) - float(self.min_value)) \
                + self.min_value

    def _on_keydown(self, event):
        if event.message == "arrow_right":
            self._set_current_val(self.currentVal + 2)
        elif event.message == "arrow_left":
            self._set_current_val(self.currentVal - 2)
        elif event.message == "escape":
            self.currentVal = self.dragStartVal
            self._stop_drag(event)
            self._update_knob()

    def _update_drag(self, event):
        if self.dragging:
            dragOffset = event.coordinates.x - self.dragStartPos.x
            finalValue = self.dragStartVal + dragOffset
            self._set_current_val(finalValue)

    def _stop_drag(self, event):
        self.dragStartPos = None
        self.dragging = False
        self.dragStartVal = self.currentVal
        self.knob.color = (1,1,1,1)


class LUISliderWithLabel(LUIObject, LUICallback):

    def __init__(self, parent=None, width=100.0, filled=False, min_value=0, max_value=1.0, precision=2, value=None):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        LUICallback.__init__(self)

        max_numbers_before = max(len(str(int(max_value))), len(str(int(min_value))))
        number_space_required = max_numbers_before

        if precision > 0:
            number_space_required += 1 + precision

        pixels_per_number = 7
        self.precision = precision

        self.slider = LUISlider(self, width=width - pixels_per_number * number_space_required - 5, filled=filled, min_value=min_value, max_value=max_value, value=value)
        self.label = LUILabel(parent=self, shadow=True, text=u"1.23")
        self.label.right = 0
        self.label.top = self.label.height - self.slider.height
        self.label.color = (1,1,1,0.5)

        self.slider.add_change_callback(self._on_slider_changed)
        self.slider.add_change_callback(self._trigger_callback)
        self._on_slider_changed(self.slider, self.slider.get_value())

        if parent is not None:
            self.parent = parent

        self.fit_to_children()

    def get_value(self):
        return self.slider.get_value()

    def set_value(self, val):
        self.slider.set_value(val)

    def _on_slider_changed(self, obj, value):
        self.label.text = ("{:." + str(self.precision) + "f}").format(value)

class LUIProgressbar(LUIObject):

    def __init__(self, parent=None, width=200, value=50, show_label=True):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)

        self.bgLeft = LUISprite(self, "ProgressbarBg_Left", "skin")
        self.bgMid = LUISprite(self, "ProgressbarBg", "skin")
        self.bgRight = LUISprite(self, "ProgressbarBg_Right", "skin")

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.fgLeft = LUISprite(self, "ProgressbarFg_Left", "skin")
        self.fgMid = LUISprite(self, "ProgressbarFg", "skin")
        self.fgRight = LUISprite(self, "ProgressbarFg_Right", "skin")
        self.fgFinish = LUISprite(self, "ProgressbarFg_Finish", "skin")

        self.showLabel = show_label
        self.progressPixel = 0
        self.fgFinish.right = 0

        self.fit_to_children()

        if self.showLabel:
            self.progressLabel = LUILabel(parent=self, text=u"33 %", shadow=True)
            self.progressLabel.centered = (True, False)
            self.progressLabel.top = -1

        self.set_value(value)
        self._update_progress()

        if parent is not None:
            self.parent = parent

    def set_value(self, val):
        val = max(0, min(100, val))
        self.progressPixel = int(val / 100.0 * self.width)
        self._update_progress()

    def _update_progress(self):
        self.fgFinish.hide()

        if self.progressPixel <= self.fgLeft.width + self.fgRight.width:
            self.fgMid.hide()
            self.fgRight.left = self.fgLeft.width
        else:
            self.fgMid.show()
            self.fgMid.left = self.fgLeft.width
            self.fgMid.width = self.progressPixel - self.fgRight.width - self.fgLeft.width
            self.fgRight.left = self.fgMid.left + self.fgMid.width

            if self.progressPixel >= self.width - self.fgRight.width:
                self.fgFinish.show()
                self.fgFinish.right = - (self.width - self.progressPixel)
                self.fgFinish.clip_bounds = (0, self.width - self.progressPixel, 0, 0)

        if self.showLabel:
            percentage = self.progressPixel / self.width * 100.0
            self.progressLabel.set_text(unicode(int(percentage)) + u" %")

class LUIInputField(LUIObject, LUICallback):

    def __init__(self, parent=None, width=200, placeholder=u"Enter some text ..", value=u""):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        LUICallback.__init__(self)

        self.bgLeft = LUISprite(self, "InputField_Left", "skin")
        self.bgMid = LUISprite(self, "InputField", "skin")
        self.bgRight = LUISprite(self, "InputField_Right", "skin")

        self.textContent = LUIObject(self)
        self.textContent.margin = (5, 8, 5, 8)
        self.textContent.clip_bounds = (0,0,0,0)
        self.textContent.height = self.bgMid.height - 10
        self.textContent.width = self.width - 16

        self.textScroller = LUIObject(parent=self.textContent, x=0, y=0)
        self.text = LUILabel(parent=self.textScroller, text=u"", shadow=True)

        self.cursor = LUISprite(
            self.textScroller, "blank", "skin", x=0, y=0, w=2, h=15.0)
        self.cursor.color = (0.5, 0.5, 0.5)
        self.cursor.margin_top = 3
        self.cursor.z_offset = 20
        self.cursor_index = 0
        self.cursor.hide()

        self.value = value

        self.placeholder = LUILabel(parent=self.textContent, text=placeholder, shadow=False)
        self.placeholder.color = (1,1,1,0.5)

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        if len(self.value) > 0:
            self.placeholder.hide()

        self.tickrate = 1.0
        self.tickstart = 0.0

        self.fit_to_children()
        self._render_text()

        if parent is not None:
            self.parent = parent

    def _set_cursor_pos(self, pos):
        self.cursor_index = max(0, min(len(self.value), pos))
        self._reset_cursor_tick()

    def on_tick(self, event):
        frametime = globalClock.getFrameTime() - self.tickstart
        show_cursor = frametime % self.tickrate < 0.5 * self.tickrate
        if show_cursor:
            self.cursor.color = (0.5,0.5,0.5,1)
        else:
            self.cursor.color = (1,1,1,0)

    def _add_text(self, text):
        self.value = self.value[:self.cursor_index] + text + self.value[self.cursor_index:]
        self._set_cursor_pos(self.cursor_index + len(text))
        self._render_text()

    def on_click(self, event):
        self.request_focus()

    def on_mousedown(self, event):
        local_x_offset = self.text.text.get_relative_pos(event.coordinates).x
        self._set_cursor_pos(self.text.text.get_char_index(local_x_offset))
        self._render_text()

    def _reset_cursor_tick(self):
        self.tickstart = globalClock.getFrameTime()

    def on_focus(self, event):
        self.cursor.show()
        self.placeholder.hide()
        self._reset_cursor_tick()

        self.bgLeft.color  = (0.9,0.9,0.9,1)
        self.bgMid.color   = (0.9,0.9,0.9,1)
        self.bgRight.color = (0.9,0.9,0.9,1)

    def on_keydown(self, event):
        key_name = event.get_message()
        if key_name == "backspace":
            self.value = self.value[:max(0, self.cursor_index - 1)] + self.value[self.cursor_index:]
            self._set_cursor_pos(self.cursor_index - 1)
            self._trigger_callback(self.value)
            self._render_text()
        elif key_name == "delete":
            self.value = self.value[:self.cursor_index] + self.value[min(len(self.value), self.cursor_index + 1):]
            self._set_cursor_pos(self.cursor_index)
            self._trigger_callback(self.value)
            self._render_text()
        elif key_name == "arrow_left":
            self._set_cursor_pos(self.cursor_index - 1)
            self._render_text()
        elif key_name == "arrow_right":
            self._set_cursor_pos(self.cursor_index + 1)
            self._render_text()

    def on_keyrepeat(self, event):
        self.on_keydown(event)

    def on_textinput(self, event):
        self._add_text(event.get_message())
        self._trigger_callback(self.value)

    def on_blur(self, event):
        self.cursor.hide()
        if len(self.value) < 1:
            self.placeholder.show()

        self.bgLeft.color = (1,1,1,1)
        self.bgMid.color = (1,1,1,1)
        self.bgRight.color = (1,1,1,1)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        # QUESTION: Should we trigger a callback when the user changes the value hisself?
        self._trigger_callback(self.value)
        self._render_text()

    def _render_text(self):
        self.text.set_text(self.value)
        self.cursor.left = self.text.left + self.text.text.get_char_pos(self.cursor_index) + 1
        max_left = self.width - 20

        # Scroll if the cursor is outside of the clip bounds
        relX = self.get_relative_pos(self.cursor.get_abs_pos()).x
        if relX >= max_left:
            self.textScroller.left = min(0, max_left - self.cursor.left)
        if relX <= 0:
            self.textScroller.left = min(0, - self.cursor.left - relX)





class LUIKeyMarker(LUIObject):

    def __init__(self, parent=None, key=u"A"):
        LUIObject.__init__(self)
        self.bgLeft = LUISprite(self, "Keymarker_Left", "skin")
        self.bgMid = LUISprite(self, "Keymarker", "skin")
        self.bgRight = LUISprite(self, "Keymarker_Right", "skin")

        self.label = LUILabel(parent=self, text=key, shadow=True)
        self.label.centered = (True, True)
        self.label.margin = (-3, 0, 0, -1)
        self.margin = (-1, 0, 0, -1)

        self.set_key(key)

        if parent is not None:
            self.parent = parent

        self.fit_to_children()

    def set_key(self, key):
        self.label.set_text(key)
        self.width = self.label.width + self.bgLeft.width + self.bgRight.width + 7
        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.fit_to_children()

class LUIKeyInstruction(LUIObject):

    def __init__(self, parent=None, key=u"A", instruction=u"Instruction"):
        LUIObject.__init__(self)
        self.marker = LUIKeyMarker(parent=self, key=key)
        self.instructionLabel = LUILabel(parent=self, text=instruction, shadow=True)
        self.instructionLabel.centered = (False, True)
        self.instructionLabel.margin_top = -4
        self.set_key(key)

    def set_key(self, key):
        self.marker.set_key(key)
        self.instructionLabel.left = self.marker.width + 5
        self.fit_to_children()


class LUIScrollableRegion(LUIObject):

    def __init__(self, parent, width=100, height=100, padding=10):
        LUIObject.__init__(self, x=0, y=0, w=width, h=height)

        self.contentParent = LUIObject(self, x=0, y=0, w=width, h=height)
        self.contentParent.clip_bounds = (0,0,0,0)

        self.contentClip = LUIObject(self.contentParent, x=padding, y=padding, w=self.width - 2*padding, h=self.height - 2*padding)
        self.contentScroller = LUIObject(self.contentClip, x=0, y=0, w=self.contentClip.width, h=500)

        self.scrollbar = LUIObject(self, x=0, y=0, w=20, h=self.height)
        self.scrollbar.right = -10

        self.scrollbarHeight = self.height
        self.scrollbarBg = LUISprite(self.scrollbar, "blank", "skin")
        self.scrollbarBg.color = (1,1,1,0.1)
        self.scrollbarBg.size = (5, self.scrollbarHeight)
        self.scrollbarBg.left = 8


        # Handle
        self.scrollbarHandle = LUIObject(self.scrollbar, x=5, y=0, w=10, h=100)
        self.scrollHandleTop = LUISprite(self.scrollbarHandle, "ScrollbarHandle_Top", "skin")
        self.scrollHandleMid = LUISprite(self.scrollbarHandle, "ScrollbarHandle", "skin")
        self.scrollHandleBottom = LUISprite(self.scrollbarHandle, "ScrollbarHandle_Bottom", "skin")

        self.scrollbarHandle.bind("mousedown", self._start_scrolling)
        self.scrollbarHandle.bind("mouseup", self._stop_scrolling)
        self.scrollbar.bind("mousedown", self._on_bar_click)
        self.scrollbar.bind("mouseup", self._stop_scrolling)

        self.handleDragging = False
        self.dragStartY = 0

        self.scrollTopPosition = 0
        self.contentHeight = 400

        scrollShadowWidth = self.width - 10

        # Top shadow
        self.scrollShadowTop = LUIObject(self)
        self.scrollShadowTopLeft = LUISprite(self.scrollShadowTop, "ScrollShadow_BL", "skin")
        self.scrollShadowTopMid = LUISprite(self.scrollShadowTop, "ScrollShadow_Bottom", "skin")
        self.scrollShadowTopRight = LUISprite(self.scrollShadowTop, "ScrollShadow_BR", "skin")
        self.scrollShadowTopMid.left = self.scrollShadowTopLeft.width
        self.scrollShadowTopMid.width = scrollShadowWidth - self.scrollShadowTopLeft.width - self.scrollShadowTopRight.width
        self.scrollShadowTopRight.left = self.scrollShadowTopMid.left + self.scrollShadowTopMid.width

        # Bottom shadow
        self.scrollShadowBottom = LUIObject(self)
        self.scrollShadowBottomLeft = LUISprite(self.scrollShadowBottom, "ScrollShadow_TL", "skin")
        self.scrollShadowBottomMid = LUISprite(self.scrollShadowBottom, "ScrollShadow_Top", "skin")
        self.scrollShadowBottomRight = LUISprite(self.scrollShadowBottom, "ScrollShadow_TR", "skin")
        self.scrollShadowBottomMid.left = self.scrollShadowBottomLeft.width
        self.scrollShadowBottomMid.width = scrollShadowWidth - self.scrollShadowBottomLeft.width - self.scrollShadowBottomRight.width
        self.scrollShadowBottomRight.left = self.scrollShadowBottomMid.left + self.scrollShadowBottomMid.width
        self.scrollShadowBottom.bottom = 0
        self.scrollShadowBottomLeft.bottom = 0
        self.scrollShadowBottomMid.bottom = 0
        self.scrollShadowBottomRight.bottom = 0

        self.handleHeight = 100
        self._update()


        if parent is not None:
            self.parent = parent

    def _on_bar_click(self, event):
        self._scroll_to_bar_pixels(event.coordinates.y - self.scrollbar.abs_pos.y - self.handleHeight / 2.0)
        self._update()
        self._start_scrolling(event)

    def _start_scrolling(self, event):
        self.request_focus()
        if not self.handleDragging:
            self.dragStartY = event.coordinates.y
            self.handleDragging = True

    def _stop_scrolling(self, event):
        if self.handleDragging:
            self.handleDragging = False
            self.blur()

    def _scroll_to_bar_pixels(self, pixels):
        offset = pixels * self.contentHeight / self.height
        self.scrollTopPosition = offset
        self.scrollTopPosition = max(0, min(self.contentHeight - self.contentClip.height, self.scrollTopPosition))

    def on_tick(self, event):
        if self.handleDragging:
            scroll_abs_pos = self.scrollbar.abs_pos
            clampedCoordY = max(scroll_abs_pos.y, min(scroll_abs_pos.y + self.scrollbarHeight, event.coordinates.y))
            offset = clampedCoordY - self.dragStartY
            self.dragStartY = clampedCoordY
            self._scroll_to_bar_pixels(self.scrollTopPosition/self.contentHeight*self.height + offset)
        self._update()

    def _set_handle_height(self, height):
        self.scrollHandleMid.top = self.scrollHandleTop.height
        self.scrollHandleMid.height = height - self.scrollHandleTop.height - self.scrollHandleBottom.height
        self.scrollHandleBottom.top = self.scrollHandleMid.height + self.scrollHandleMid.top
        self.handleHeight = height

    def _update(self):
        self.contentScroller.top = -self.scrollTopPosition
        scrollbarHeight = max(0.1, min(1.0, self.contentClip.height / self.contentHeight))
        scrollbarHeightPixels = scrollbarHeight * self.height
        self._set_handle_height(scrollbarHeightPixels)
        self.scrollbarHandle.top = self.scrollTopPosition / self.contentHeight * self.height

        topAlpha = max(0.0, min(1.0, self.scrollTopPosition / 50.0))
        bottomAlpha = max(0.0, min(1.0, (self.contentHeight - self.scrollTopPosition - self.contentClip.height) / 50.0 ))
        self.scrollShadowTop.color = (1,1,1,topAlpha)
        self.scrollShadowBottom.color = (1,1,1,bottomAlpha)

    def get_content_node(self):
        return self.contentScroller


class LUIColorpicker(LUIObject):

    def __init__(self, parent=None, color=None):
        LUIObject.__init__(self, x=0, y=0, w=27, h=27)

        self.previewBg = LUISprite(self, "ColorpickerPreviewBg", "skin")

        self.filler = LUISprite(self, "blank", "skin")
        self.filler.width = 21
        self.filler.height = 21
        self.filler.pos = (5, 5)
        self.filler.color = (0.2,0.6,1.0,1.0)

        self.overlay = LUISprite(self, "ColorpickerPreviewOverlay", "skin")
        self.overlay.pos = (2, 2)
        self.overlay.bind("click", self._open_dialog)

        self.fit_to_children()

        self.popup = LUIColorpickerPopup(self)
        self.popup.hide()

        if color is not None:
            self.colorValue = color
        else:
            # My favourite color
            self.colorValue = (0.2, 0.6, 1.0)
        self.set_color_value(self.colorValue)

        self.popup.add_change_callback(self._on_popup_color_changed)

        if parent is not None:
            self.parent = parent

    def _open_dialog(self, event):
        if self.has_focus():
            self.blur()
        else:
            self.request_focus()

    def on_focus(self, event):
        self.popup._load_rgb(self.colorValue)
        self.popup.open_at(self, 14.0)

    def set_color_value(self, rgb):
        self.colorValue = rgb
        self.filler.color = rgb

    def get_color_value(self):
        return self.colorValue

    def on_tick(self, event):
        self.popup._update(event)

    def on_blur(self, event):
        self.popup.close()

    def _on_popup_color_changed(self, popup, rgb):
        self.set_color_value(rgb)

    def _on_popup_closed(self):
        self.blur()


class LUIPopup(LUIFrame):

    def __init__(self, parent=None, width=200, height=200):
        LUIFrame.__init__(self, parent=parent, width=width, height=height, padding=10, innerPadding=0)
        self.topmost = True
        self.borderSize = 33
        self.content.bind("click", self._on_content_click)

    def open_at(self, targetElement, distance):
        self.show()

        targetPos = targetElement.get_abs_pos()+ targetElement.get_size() / 2

        showAbove = targetPos.y > self.height - self.borderSize
        showLeft = targetPos.x > self.width - self.borderSize

        relative = self.get_relative_pos(targetPos)
        self.pos += relative

        if showLeft:
            self.left -= self.width - self.borderSize
            self.left += 25
        else:
            self.left -= self.borderSize
            self.left -= 25

        if showAbove:
            self.top -= distance
            self.top -= self.height - self.borderSize
        else:
            self.top += distance
            self.top -= self.borderSize


    def _on_content_click(self, event):
        pass

    def close(self):
        self.hide()

class LUIColorpickerPopup(LUIPopup, LUICallback):
    def __init__(self, parent=None):
        LUIPopup.__init__(self, parent=parent, width=240, height=146)
        LUICallback.__init__(self)

        self.field = LUIObject(self.content, x=0, y=0, w=128, h=128)

        self.fieldBG = LUISprite(self.field, "blank", "skin")
        self.fieldBG.size = (128, 128)
        self.fieldBG.color = (0.2,0.6,1.0)
        self.fieldFG = LUISprite(self.field, "ColorpickerFieldOverlay", "skin")
        self.fieldFG.pos = (-2, 0)

        self.fieldBG.bind("mousedown", self._start_field_dragging)
        self.fieldBG.bind("mouseup", self._stop_field_dragging)

        self.fieldHandle = LUISprite(self.field, "ColorpickerFieldHandle", "skin")
        self.fieldHandle.bind("mousedown", self._start_field_dragging)
        self.fieldHandle.bind("mouseup", self._stop_field_dragging)

        self.fieldDragging = False

        self.hueSlider = LUIObject(self.content, x=140, y=0, w=40, h=128)
        self.hueSliderFG = LUISprite(self.hueSlider, "ColorpickerHueSlider", "skin")

        self.hueHandle = LUISprite(self.hueSlider, "ColorpickerHueHandle", "skin")
        self.hueHandle.left = (self.hueSliderFG.width - self.hueHandle.width) / 2.0
        self.hueHandle.top = 50

        self.hueDragging = False
        self.hueSlider.bind("mousedown", self._start_hue_dragging)
        self.hueSlider.bind("mouseup", self._stop_hue_dragging)

        self.labels = LUIVerticalLayout(self.content, width=40)
        self.labels.pos = (177, 42)

        colors = [u"R", u"G", u"B"]
        self.colorLabels = []

        for color in colors:
            label = LUILabel(text=color, shadow=True)
            label.color =  (1,1,1,0.3)

            valueLabel = LUILabel(text=u"255", shadow=True)
            valueLabel.right = 0
            self.labels.add(label, valueLabel)
            self.colorLabels.append(valueLabel)

        self.activeColor = LUIObject(self.content, x=177, y=0)
        self.activeColorBG = LUISprite(self.activeColor, "blank", "skin")
        self.activeColorFG = LUISprite(self.activeColor, "ColorpickerActiveColorOverlay", "skin")

        self.activeColorBG.size = (40, 40)
        self.activeColorBG.pos = (2, 0)
        self.activeColorBG.color = (0.2,0.6,1.0,1.0)

        self.closeButton = LUIButton(parent=self.content, text=u"Done", width=45, template="ButtonMagic")
        self.closeButton.left = 177
        self.closeButton.top = 98
        self.closeButton.bind("click", self._close_popup)

        self._set_hue(0.5)
        self._set_sat_val(0.5, 0.5)

        self.widget = parent

    def _load_rgb(self, rgb):
        hsv = colorsys.rgb_to_hsv(*rgb)
        self._set_hue(hsv[0])
        self._set_sat_val(hsv[1], hsv[2])

    def _close_popup(self, event):
        self.widget._on_popup_closed()
        self.close()

    def _update(self, event):
        if self.hueDragging:
            offset = event.coordinates.y - self.hueSliderFG.abs_pos.y
            offset /= 128.0
            offset = 1.0 - max(0.0, min(1.0, offset))
            self._set_hue(offset)

        if self.fieldDragging:
            offset = event.coordinates - self.fieldBG.abs_pos
            saturation = max(0.0, min(1.0, offset.x / 128.0))
            value = 1.0 - max(0.0, min(1.0, offset.y / 128.0))
            self._set_sat_val(saturation, value)

        self._update_color()

    def _set_sat_val(self, sat, val):
        self.saturation = sat
        self.valueValue = val

        self.fieldHandle.top = (1.0 - self.valueValue) * 128.0 - self.fieldHandle.height / 2.0
        self.fieldHandle.left = self.saturation * 128.0 - self.fieldHandle.width / 2.0

    def _set_hue(self, hue):
        self.hueValue = min(0.999, hue)
        self.hueHandle.top = (1.0-hue) * 128.0 - self.hueHandle.height / 2
        self.fieldBG.color = colorsys.hsv_to_rgb(self.hueValue, 1, 1)

    def _update_color(self):
        rgb = colorsys.hsv_to_rgb(self.hueValue, self.saturation, self.valueValue)
        self.activeColorBG.color = rgb

        self.colorLabels[0].set_text(unicode(int(rgb[0]*255.0)))
        self.colorLabels[1].set_text(unicode(int(rgb[1]*255.0)))
        self.colorLabels[2].set_text(unicode(int(rgb[2]*255.0)))

        self._trigger_callback(rgb)

    def _start_field_dragging(self, event):
        if not self.fieldDragging:
            self.fieldDragging = True

    def _stop_field_dragging(self, event):
        if self.fieldDragging:
            self.fieldDragging = False

    def _start_hue_dragging(self, event):
        if not self.hueDragging:
            self.hueDragging = True

    def _stop_hue_dragging(self, event):
        if self.hueDragging:
            self.hueDragging = False


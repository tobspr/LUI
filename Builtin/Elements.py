from panda3d.lui import *
from panda3d.core import Point2

from functools import partial
from Layouts import *

import math
import colorsys

class UICallback:

    def __init__(self):
        self.changeCallbacks = []

    def add_change_callback(self, cb):
        if cb not in self.changeCallbacks:
            self.changeCallbacks.append(cb)

    def remove_change_callback(self, cb):
        if cb in self.changeCallbacks:
            self.changeCallbacks.remove(cb)

    def _trigger_callback(self, *args, **kwargs):
        for cb in self.changeCallbacks:
            cb(*args, **kwargs)

class UICheckbox(LUIObject, UICallback):

    def __init__(self, parent=None, checked=False):
        LUIObject.__init__(self)
        UICallback.__init__(self)

        self.sprite = LUISprite(self, "Checkbox_Default", "skin")
        self.fit_to_children()
        self.checked = checked
        self._update_sprite()

        if parent is not None:
            self.parent = parent

    def on_click(self, event):
        self.checked = not self.checked
        self._trigger_callback(self, self.checked)
        self._update_sprite()

    def on_mousedown(self, event):
        self.color = (0.86,0.86,0.86,1.0)

    def on_mouseup(self, event):
        self.color = (1,1,1,1)

    def is_checked(self):
        return self.checked

    def set_checked(self, checked):
        self.checked = checked
        self._update_sprite()

    def _update_sprite(self):
        img = "Checkbox_Checked" if self.checked else "Checkbox_Default"
        self.sprite.set_texture(img, "skin")

class UILabel(LUIObject):

    def __init__(self, parent=None, text=u"Label", shadow=True, font_size=14, font="label"):

        LUIObject.__init__(self)

        # self.hide()
        self.text = LUIText(self, text, font, font_size, 0, 0)
        self.text.color = (1,1,1,0.9)
        self.text.z_offset = 1

        self.have_shadow = shadow

        if self.have_shadow:
            self.shadowText = LUIText(self, unicode(text), font, font_size, 0, 0)
            self.shadowText.top = 1
            self.shadowText.color = (0,0,0,0.7)

        self.fit_to_children()

        if parent is not None:
            self.parent = parent

    def set_text(self, text):

        self.text.text = unicode(text)
        if self.have_shadow:
            self.shadowText.text = unicode(text)
        self.fit_to_children()

class UILabeledCheckbox(LUIObject, UICallback):
    
    def __init__(self, parent=None, checked=False, text=u"Checkbox"):
        LUIObject.__init__(self)    
        UICallback.__init__(self)

        self.checkbox = UICheckbox(parent=self, checked=checked)
        self.label = UILabel(parent=self, text=text, shadow=True)
        self.label.bind("click", self.checkbox.on_click)
        self.label.bind("mousedown", self.checkbox.on_mousedown)
        self.label.bind("mouseup", self.checkbox.on_mouseup)

        self.checkbox.add_change_callback(self._trigger_callback)

        if parent is not None:
            self.parent = parent

        self.label.left = self.checkbox.width + 6
        self.label.top = self.label.height - self.checkbox.height

        self.fit_to_children()

    def get_box(self):
        return self.checkbox

class UIRadioboxGroup(LUIObject):

    def __init__(self):
        self.boxes = []
        self.selected_box = None

    def register_box(self, box):
        if box not in self.boxes:
            self.boxes.append(box)

    def set_active(self, active_box):
        for box in self.boxes:
            if box is not active_box:
                box._update_state(False)
            else:
                box._update_state(True)
        self.selected_box = active_box

    def get_active_box(self):
        return self.selected_box

    def get_active_value(self):
        if self.selected_box is None:
            return None
        return self.selected_box.get_value()


class UIRadiobox(LUIObject, UICallback):

    def __init__(self, parent=None, group=None, value=5):
        LUIObject.__init__(self)
        UICallback.__init__(self)

        self.sprite = LUISprite(self, "Radiobox_Default", "skin")
        self.fit_to_children()
        self.group = group
        self.group.register_box(self)
        self.active = False
        self.value = value

        if parent is not None:
            self.parent = parent

    def on_click(self, event):
        self.set_active()

    def set_active(self):
        if self.group is not None:
            self.group.set_active(self)
        else:
            self.active = True
            self._update_sprite()

    def get_value(self):
        return self.value

    def _update_state(self, active):
        self.active = active
        self._trigger_callback(self, self.active)
        self._update_sprite()

    def on_mousedown(self, event):
        self.color = (0.86,0.86,0.86,1.0)
        # pass

    def on_mouseup(self, event):
        self.color = (1,1,1,1)

    def _update_sprite(self):
        img = "Radiobox_Active" if self.active else "Radiobox_Default"
        self.sprite.set_texture(img, "skin")


class UILabeledRadiobox(LUIObject, UICallback):
    
    def __init__(self, parent=None, group=None, value=None, text=u"Radiobox"):
        LUIObject.__init__(self)    
        UICallback.__init__(self)

        self.radiobox = UIRadiobox(parent=self, group=group, value=value)
        self.label = UILabel(parent=self, text=text, shadow=True)
        self.label.bind("click", self.radiobox.on_click)
        self.label.bind("mousedown", self.radiobox.on_mousedown)
        self.label.bind("mouseup", self.radiobox.on_mouseup)
        self.radiobox.add_change_callback(self._trigger_callback)

        if parent is not None:
            self.parent = parent

        self.label.left = self.radiobox.width + 6
        self.label.top = self.label.height - self.radiobox.height
        self.fit_to_children()


    def get_box(self):
        return self.radiobox

class UISlider(LUIObject, UICallback):

    def __init__(self, parent=None, filled=False, min_value=0.0, max_value=1.0, width=100.0, value=None):

        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        UICallback.__init__(self)
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
        self._trigger_callback(self, self.get_value())
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


class UISliderWithLabel(LUIObject, UICallback):

    def __init__(self, parent=None, width=100.0, filled=False, min_value=0, max_value=1.0, precision=2, value=None):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        UICallback.__init__(self)

        max_numbers_before = max(len(str(int(max_value))), len(str(int(min_value))))
        number_space_required = max_numbers_before

        if precision > 0:
            number_space_required += 1 + precision

        pixels_per_number = 7
        self.precision = precision

        self.slider = UISlider(self, width=width - pixels_per_number * number_space_required - 5, filled=filled, min_value=min_value, max_value=max_value, value=value)
        self.label = UILabel(parent=self, shadow=True, text=u"1.23")
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
        self.label.set_text( ("{:." + str(self.precision) + "f}").format(value))

class UIProgressbar(LUIObject):

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
            self.progressLabel = UILabel(parent=self, text=u"33 %", shadow=True)
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

class UIInputField(LUIObject, UICallback):

    def __init__(self, parent=None, width=200, placeholder=u"Enter some text ..", value=u""):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        UICallback.__init__(self)

        self.bgLeft = LUISprite(self, "InputField_Left", "skin")
        self.bgMid = LUISprite(self, "InputField", "skin")
        self.bgRight = LUISprite(self, "InputField_Right", "skin")

        self.textContent = LUIObject(self)    
        self.textContent.margin = (5, 8, 5, 8)
        self.textContent.clip_bounds = (0,0,0,0)
        self.textContent.height = self.bgMid.height - 10
        self.textContent.width = self.width - 16

        self.textScroller = LUIObject(parent=self.textContent, x=0, y=0)
        self.text = UILabel(parent=self.textScroller, text=u"", shadow=True)

        self.cursor = LUISprite(
            self.textScroller, "blank", "skin", x=0, y=0, w=2, h=15.0)
        self.cursor.color = (0.5, 0.5, 0.5)
        self.cursor.margin_top = 3
        self.cursor.z_offset = 20
        self.cursor_index = 0
        self.cursor.hide()

        self.value = value

        self.placeholder = UILabel(parent=self.textContent, text=placeholder, shadow=False)
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
            self._trigger_callback(self, self.value)
            self._render_text()
        elif key_name == "delete":
            self.value = self.value[:self.cursor_index] + self.value[min(len(self.value), self.cursor_index + 1):]
            self._set_cursor_pos(self.cursor_index)
            self._trigger_callback(self, self.value)
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
        self._trigger_callback(self, self.value)

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
        self._trigger_callback(self, self.value)
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

class UISelectbox(LUIObject, UICallback):

    def __init__(self, parent=None, width=200, options=None, selectedOption=None):
        LUIObject.__init__(self, x=0, y=0, w=width+4, h=0)
        UICallback.__init__(self)

        # The selectbox has a small border, to correct this we move it
        self.margin_left = -2

        self.bgLeft = LUISprite(self, "Selectbox_Left", "skin")
        self.bgMid = LUISprite(self, "Selectbox", "skin")
        self.bgRight = LUISprite(self, "Selectbox_Right", "skin")

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.bgRight.z_offset = 1

        self.labelContainer = LUIObject(self, x=10, y=6, w=width - 20 - self.bgRight.width, h=self.bgMid.height - 6)
        self.labelContainer.clip_bounds = (0,0,0,0)

        self.label = UILabel(parent=self.labelContainer, text=u"Select an option ..", shadow=True)

        self.bgRight.bind("mouseover", self._knob_mouseover)
        self.bgRight.bind("mouseout", self._knob_mouseout)
        self.bgRight.bind("click", self.on_click)
        self.bgRight.bind("click", self.on_click)

        self.fit_to_children()

        self.dropMenu = UISelectdrop(parent=self, width=width)
        self.dropMenu.top = self.bgMid.height - 7
        self.dropMenu.topmost = True

        self.dropOpen = False
        self.dropMenu.hide()

        self.options = []
        self.currentOptionId = None

        if options is not None:
            self.options = options

        self._select_option(selectedOption)

    def get_selected_option(self):
        return self.currentOptionId

    def _render_options(self):
        self.dropMenu._render_options(self.options)

    def set_options(self, options):
        self._render_options()

    def _select_option(self, optid):
        self.label.color = (1,1,1,1)
        for optID, optVal in self.options:
            if optID == optid:
                self.label.set_text(optVal)
                self.currentOptionId = optID
                return
        self.label.color = (1,1,1,0.5)

    def _knob_mouseover(self, event):
        self.bgRight.color = (0.9,0.9,0.9,1.0)

    def _knob_mouseout(self, event):
        self.bgRight.color = (1,1,1,1.0)

    def on_click(self, event):
        self.request_focus()
        if self.dropOpen:
            self._close_drop()
        else:
            self._open_drop()

    def on_mousedown(self, event):
        self.bgLeft.color = (0.9,0.9,0.9,1.0)
        self.bgMid.color = (0.9,0.9,0.9,1.0)

    def on_mouseup(self, event):
        self.bgLeft.color = (1,1,1,1.0)
        self.bgMid.color = (1,1,1,1.0)

    def _open_drop(self):
        if not self.dropOpen:
            self._render_options()
            self.dropMenu.show()
            self.request_focus()

            self.dropOpen = True

    def _close_drop(self):
        if self.dropOpen:
            self.dropMenu.hide()

            self.dropOpen = False

    def _on_option_selected(self, optid):
        self._select_option(optid)
        self._close_drop()

    def on_blur(self, event):
        self._close_drop()


class UISelectdrop(LUIObject):

    def __init__(self, parent, width=200):
        LUIObject.__init__(self, x=0, y=0, w=width, h=1)

        self.layout = UICornerLayout(self, "Selectdrop_", width + 10, 100)
        self.layout.margin_left = -3

        self.opener = LUISprite(self, "SelectboxOpen_Right", "skin")
        self.opener.right = -4
        self.opener.top = -25
        self.opener.z_offset = 3

        self.container = LUIObject(self.layout, 0, 0, 0, 0)
        self.container.width = self.width
        self.container.clip_bounds = (0,0,0,0)
        self.container.left = 5

        self.selectbox = parent
        self.parent = self.selectbox

    def _on_opt_over(self, event):
        event.sender.color = (0,0,0,0.1)

    def _on_opt_out(self, event):
        event.sender.color = (0,0,0,0)

    def _on_opt_click(self, optid, event):
        self.selectbox._on_option_selected(optid)

    def _render_options(self, options):
        visible = min(4, len(options))
        offsetTop = 6
        self.layout.height = visible * 30 + offsetTop + 11
        self.container.height = visible * 30 + offsetTop + 1
        self.layout.update_layout()
        self.container.remove_all_children()
        
        currentY = offsetTop
        for optId, optVal in options:
            optContainer = LUIObject(self.container, x=0, y=currentY, w=self.container.width - 30, h=30)

            optBg = LUISprite(optContainer, "blank", "skin")
            optBg.width = self.container.width
            optBg.height = optContainer.height
            optBg.color = (0,0,0,0)
            optBg.bind("mouseover", self._on_opt_over)
            optBg.bind("mouseout", self._on_opt_out)
            optBg.bind("click", partial(self._on_opt_click, optId))

            optLabel = UILabel(parent=optContainer, text=unicode(optVal), shadow=True)
            optLabel.top = 5
            optLabel.left = 8

            if optId == self.selectbox.get_selected_option():
                optLabel.color = (0.6, 0.9, 0.4, 1.0)

            divider = LUISprite(optContainer, "SelectdropDivider", "skin")
            divider.top = 30 - divider.height / 2
            divider.width = self.container.width

            currentY += 30


class UIButton(LUIObject):

    def __init__(self, parent=None, text=u"Button", width=200, template="ButtonDefault"):

        LUIObject.__init__(self, x=0, y=0, w=width+2, h=0)

        self.margin_left = -1

        self.template = template
        self.bgLeft = LUISprite(self, template + "_Left", "skin")
        self.bgMid = LUISprite(self, template, "skin")
        self.bgRight = LUISprite(self, template + "_Right", "skin")

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.label = UILabel(parent=self, text=text, shadow=True)
        self.label.centered = (True, True)
        self.label.margin_top = -3
        self.label.margin_left = -1

        if parent is not None:
            self.parent = parent

        self.fit_to_children()

    def set_text(self, text):
        self.label.set_text(text)

    def on_mousedown(self, event):
        self.bgLeft.set_texture(self.template + "Focus_Left", "skin", resize=False)
        self.bgMid.set_texture(self.template + "Focus", "skin", resize=False)
        self.bgRight.set_texture(self.template + "Focus_Right", "skin", resize=False)
        self.label.margin_top = -2

    def on_mouseup(self, event):
        self.bgLeft.set_texture(self.template + "_Left", "skin", resize=False)
        self.bgMid.set_texture(self.template, "skin", resize=False)
        self.bgRight.set_texture(self.template + "_Right", "skin", resize=False)
        self.label.margin_top = -3



class UIKeyMarker(LUIObject):
    
    def __init__(self, parent=None, key=u"A"):
        LUIObject.__init__(self)
        self.bgLeft = LUISprite(self, "Keymarker_Left", "skin")
        self.bgMid = LUISprite(self, "Keymarker", "skin")
        self.bgRight = LUISprite(self, "Keymarker_Right", "skin")

        self.label = UILabel(parent=self, text=key, shadow=True)
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

class UIKeyInstruction(LUIObject):

    def __init__(self, parent=None, key=u"A", instruction=u"Instruction"):
        LUIObject.__init__(self)
        self.marker = UIKeyMarker(parent=self, key=key)
        self.instructionLabel = UILabel(parent=self, text=instruction, shadow=True)
        self.instructionLabel.centered = (False, True)
        self.instructionLabel.margin_top = -4
        self.set_key(key)

    def set_key(self, key):
        self.marker.set_key(key)
        self.instructionLabel.left = self.marker.width + 5
        self.fit_to_children()

class UIFrame(UICornerLayout):
    def __init__(self, parent=None, width=200, height=200, padding=15):
        borderSize = 33
        effectivePadding = borderSize + padding
        UICornerLayout.__init__(self, parent=parent, image_prefix="Frame_", width=width+2*effectivePadding, height=height+2*effectivePadding)
        self.content = LUIObject(self)
        self.content.size = (width+2*padding, height+2*padding)
        self.content.pos = (borderSize, borderSize)
        self.content.padding = (padding, padding, padding, padding)
        self.content.clip_bounds = (0,0,0,0)
        self.margin = (-borderSize, -borderSize, -borderSize, -borderSize)

    def get_content_node(self):
        return self.content


class UIColorpicker(LUIObject):

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

        self.popup = UIColorpickerPopup(self)
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


class UIPopup(UIFrame):

    def __init__(self, parent=None, width=200, height=200):
        UIFrame.__init__(self, parent, width=width, height=height, padding=10)
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

class UIColorpickerPopup(UIPopup, UICallback):
    def __init__(self, parent=None):
        UIPopup.__init__(self, parent=parent, width=220, height=126)
        UICallback.__init__(self)

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

        self.labels = UIVerticalLayout(self.content, width=40)
        self.labels.pos = (177, 42)

        colors = [u"R", u"G", u"B"]
        self.colorLabels = []

        for color in colors:
            label = UILabel(text=color, shadow=True)
            label.color =  (1,1,1,0.3)

            valueLabel = UILabel(text=u"255", shadow=True)
            valueLabel.right = 0
            self.labels.add_row(label, valueLabel)
            self.colorLabels.append(valueLabel)

        self.activeColor = LUIObject(self.content, x=177, y=0)
        self.activeColorBG = LUISprite(self.activeColor, "blank", "skin")
        self.activeColorFG = LUISprite(self.activeColor, "ColorpickerActiveColorOverlay", "skin")

        self.activeColorBG.size = (40, 40)
        self.activeColorBG.pos = (2, 0)
        self.activeColorBG.color = (0.2,0.6,1.0,1.0)

        self.closeButton = UIButton(parent=self.content, text=u"Done", width=45, template="ButtonMagic")
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

        self._trigger_callback(self, rgb)

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


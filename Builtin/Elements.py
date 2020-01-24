"""



OUTDATED

Do not use anymore.


"""


import colorsys

from LUIObject import LUIObject
from LUISlider import LUISlider
from LUISprite import LUISprite
from LUIVerticalLayout import LUIVerticalLayout
from LUICallback import LUICallback
from LUILabel import LUILabel
from LUIFrame import LUIFrame
from LUIButton import LUIButton

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
        self.instructionLabel.margin.top = -4
        self.set_key(key)

    def set_key(self, key):
        self.marker.set_key(key)
        self.instructionLabel.left = self.marker.width + 5
        self.fit_to_children()


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

        self.closeButton = LUIButton(parent=self.content, text=u"Done", width=45, template="ButtonGreen")
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

        self.colorLabels[0].set_text(str(int(rgb[0]*255.0)).encode('utf-8'))
        self.colorLabels[1].set_text(str(int(rgb[1]*255.0)).encode('utf-8'))
        self.colorLabels[2].set_text(str(int(rgb[2]*255.0)).encode('utf-8'))

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


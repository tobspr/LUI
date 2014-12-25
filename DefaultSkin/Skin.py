from panda3d.lui import *


from Layouts import UIVerticalLayout

class UICheckbox(LUIObject):

    def __init__(self, parent=None, checked=False):
        LUIObject.__init__(self)

        self.sprite = LUISprite(self, "Checkbox_Default", "skin")
        self.fit_to_children()
        self.checked = checked
        self._update_sprite()

        if parent is not None:
            self.parent = parent

    def on_click(self, event):
        self.checked = not self.checked
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

    def __init__(self, parent=None, text=u"Label", shadow=True):

        LUIObject.__init__(self)

        self.text = LUIText(self, text, "label", 15.0, 0, 0)
        self.text.color = (1,1,1,0.9)
        self.text.z_offset = 5

        self.have_shadow = shadow

        if self.have_shadow:
            self.shadowText = LUIText(self, text, "label", 15.0, 0, 0)
            self.shadowText.top = 1
            self.shadowText.color = (0,0,0,1)

        self.fit_to_children()

        if parent is not None:
            self.parent = parent

    def set_text(self, text):
        self.text.text = unicode(text)
        if self.have_shadow:
            self.shadowText.text = unicode(text)
        self.fit_to_children()

class UILabeledCheckbox(LUIObject):
    
    def __init__(self, parent=None, checked=False, text=u"Checkbox"):
        LUIObject.__init__(self)    

        self.checkbox = UICheckbox(parent=self, checked=checked)
        self.label = UILabel(parent=self, text=text, shadow=True)
        self.label.bind("click", self.checkbox.on_click)
        self.label.bind("mousedown", self.checkbox.on_mousedown)
        self.label.bind("mouseup", self.checkbox.on_mouseup)

        if parent is not None:
            self.parent = parent

        self.label.left = self.checkbox.width + 6
        self.label.top = self.label.height - self.checkbox.height - 1

        self.fit_to_children()

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


class UIRadiobox(LUIObject):

    def __init__(self, parent=None, group=None, value=5):
        LUIObject.__init__(self)

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
        self._update_sprite()

    def on_mousedown(self, event):
        self.color = (0.86,0.86,0.86,1.0)
        # pass

    def on_mouseup(self, event):
        self.color = (1,1,1,1)

    def _update_sprite(self):
        img = "Radiobox_Active" if self.active else "Radiobox_Default"
        self.sprite.set_texture(img, "skin")


class UILabeledRadiobox(LUIObject):
    
    def __init__(self, parent=None, group=None, value=None, text=u"Radiobox"):
        LUIObject.__init__(self)    

        self.radiobox = UIRadiobox(parent=self, group=group, value=value)
        self.label = UILabel(parent=self, text=text, shadow=True)
        self.label.bind("click", self.radiobox.on_click)
        self.label.bind("mousedown", self.radiobox.on_mousedown)
        self.label.bind("mouseup", self.radiobox.on_mouseup)

        if parent is not None:
            self.parent = parent

        self.label.left = self.radiobox.width + 6
        self.label.top = self.label.height - self.radiobox.height - 2
        self.fit_to_children()


class UISlider(LUIObject):

    def __init__(self, parent=None, filled=False, min_value=0.0, max_value=1.0, width=100.0, value=None):

        LUIObject.__init__(self, x=0, y=0, w=width, h=0)
        self.knob = LUISprite(self, "SliderKnob", "skin")
        self.knob.z_offset = 5

        self.sliderBg = LUIObject(self, 0, 0, width, 0)
        self.bgLeft = LUISprite(self.sliderBg, "SliderBg_Left", "skin")
        self.bgRight = LUISprite(self.sliderBg, "SliderBg_Right", "skin")
        self.bgMid = LUISprite(self.sliderBg, "SliderBg", "skin")

        self.bgMid.width = width - self.bgLeft.width - self.bgRight.width
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
            self.sliderFill.z_offset = 3
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
        self.changeCallbacks = [] 

        if value is None:
            self.set_value( (self.min_value + self.max_value) / 2.0 )
        else:
            self.set_value(value)

        self.fit_to_children()
        self._update_knob()

    def _update_knob(self):
        self.knob.left = self.currentVal - (self.knob.width / 2) + self.sideMargin
        if self.filled:
            self.fillMid.width = self.currentVal - self.fillLeft.width + self.sideMargin

    def _set_current_val(self, pixels):
        pixels = max(0, min(self.effectiveWidth, pixels))
        self.currentVal = pixels

        for callback in self.changeCallbacks:
            callback(self.get_value())

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

    def add_change_callback(self, cb):
        if cb not in self.changeCallbacks:
            self.changeCallbacks.append(cb)

    def remove_change_callback(self, cb):
        if cb in self.changeCallbacks:
            self.changeCallbacks.remove(cb)

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


class UISliderWithLabel(LUIObject):

    def __init__(self, parent=None, width=100.0, filled=False, min_value=0, max_value=1.0, precision=2, value=None):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)

        max_numbers_before = max(len(str(int(max_value))), len(str(int(min_value))))
        number_space_required = max_numbers_before

        if precision > 0:
            number_space_required += 1 + precision

        pixels_per_number = 8
        self.precision = precision

        self.slider = UISlider(self, width=width - pixels_per_number * number_space_required - 5, filled=filled, min_value=min_value, max_value=max_value, value=value)
        self.label = UILabel(parent=self, shadow=True, text=u"1.23")
        self.label.right = 0
        self.label.top = self.label.height - self.slider.height - 2
        self.label.color = (1,1,1,0.5)

        self.slider.add_change_callback(self._on_slider_changed)

        self._on_slider_changed(self.slider.get_value())

        if parent is not None:
            self.parent = parent

        self.fit_to_children()

    def _on_slider_changed(self, value):
        self.label.set_text( ("{:." + str(self.precision) + "f}").format(value))

    def add_change_callback(self, cb):
        self.slider.add_change_callback(cb)

    def remove_change_callback(self, cb):
        self.slider.remove_change_callback(cb)


class UIProgressbar(LUIObject):

    def __init__(self, parent=None, width=200, value=50, show_label=True):
        LUIObject.__init__(self, x=0, y=0, w=width, h=0)    

        self.bgLeft = LUISprite(self, "ProgressbarBg_Left", "skin")
        self.bgMid = LUISprite(self, "ProgressbarBg", "skin")
        self.bgRight = LUISprite(self, "ProgressbarBg_Right", "skin")

        self.bgMid.width = width - self.bgLeft.width - self.bgRight.width
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
            self.progressLabel.top = -2

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
        
        # if self.progressPixel <= self.fgLeftWidth:
            # self.fgLeft.show()
            # self.fgLeft.width = self.progressPixel
        # else:
            # self.fgLeft.show()
            # self.fgLeft.width = self.fgLeftWidths

            # self.fgMid.width = self.progressPixel - self.fgLeft.width



if __name__ == "__main__":

    # Test script for This Skin
    from panda3d.core import *

    load_prc_file_data("", """
        text-minfilter linear
        text-magfilter linear
        text-pixels-per-unit 32
        sync-video #f
        notify-level-lui debug
        show-frame-rate-meter #t
    """)

    import direct.directbase.DirectStart

    LUIFontPool.get_global_ptr().register_font(
        "default", loader.loadFont("../Res/font/SourceSansPro-Semibold.ttf"))


    labelFont = loader.loadFont("../Res/font/SourceSansPro-Semibold.ttf")
    labelFont.setPixelsPerUnit(28)
    # labelFont.setMinfilter(SamplerState.FTNearest)
    # labelFont.setMagfilter(SamplerState.FTNearest)

    LUIFontPool.get_global_ptr().register_font(
        "label", labelFont)
    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Res/atlas.txt", "../Res/atlas.png")
    LUIAtlasPool.get_global_ptr().load_atlas(
        "skin", "res/atlas.txt", "res/atlas.png")

    base.win.set_clear_color(Vec4(1, 0, 0, 1))

    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    skinParent = LUIObject(region.root(),x=0,y=0,w=100,h=100)
    skinParent.centered = (True, True)

    layout = UIVerticalLayout(parent=skinParent, width=300, spacing=10)

    checkbox = UILabeledCheckbox(checked=False, text=u"Sample checkbox")

    group = UIRadioboxGroup()
    radiobox = UILabeledRadiobox(group=group, value=5, text=u"Value1")
    radiobox2 = UILabeledRadiobox(group=group, value=7, text=u"Value2")

    slider = UISliderWithLabel(filled=False, min_value=0.0, max_value=1.0, width=300.0, precision=4)
    slider2 = UISliderWithLabel(filled=True, min_value=0.0, max_value=100.0, width=300.0, precision=1)
    bar = UIProgressbar(width=300, value=33.5)
    slider2.add_change_callback(bar.set_value)




    layout.add_column(checkbox)
    layout.add_column(radiobox)
    layout.add_column(radiobox2)
    layout.add_column(slider)
    layout.add_column(slider2)
    layout.add_column(bar)


    skinParent.fit_to_children()

    bgFrame = LUISprite(region.root(), "blank", "default", 0, 0, 10000, 10000)
    bgFrame.bind("click", lambda event: bgFrame.request_focus())
    bgFrame.z_offset = -1
    bgFrame.color = (0.1,0.1,0.1)
    base.accept("f3", region.toggle_render_wireframe)
    base.accept("f4", region.root().ls)
    base.run()


if __name__ == "__main__":

    # Test script for This Skin
    from panda3d.core import *
    from Elements import *

    load_prc_file_data("", """
        text-minfilter linear
        text-magfilter linear
        text-pixels-per-unit 32
        sync-video #f
        notify-level-lui info
        show-frame-rate-meter #t
        win-size 800 610
    """)

    import direct.directbase.DirectStart

    from LUISkin import LUIDefaultSkin
    from LUICheckbox import LUICheckbox
    from LUIRadioboxGroup import LUIRadioboxGroup
    from LUISelectbox import LUISelectbox

    skin = LUIDefaultSkin()
    skin.load()

    base.win.set_clear_color(Vec4(0, 0, 0, 1))

    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    skinParent = LUIObject(region.root(),x=300,y=150,w=250,h=100)
    # skinParent.centered = (True, True)
    skinParent.top = 100
    skinParent.left = 300

    frame = LUIFrame(parent=skinParent, width=290, height=400, padding=20, innerPadding=20, scrollable=True)
    layout = LUIVerticalLayout(parent=frame, width=250, spacing=10)

    checkbox = LUICheckbox(checked=False, label=u"Sample checkbox")
    checkboxChecked = LUICheckbox(checked=True, label=u"Checked checkbox")

    skinParent.fit_to_children()

    group = LUIRadioboxGroup()
    radiobox = LUILabeledRadiobox(group=group, value=5, text=u"Radiobox")
    radiobox2 = LUILabeledRadiobox(group=group, value=7, text=u"Radiobox Checked")

    radiobox2.get_box().set_active()

    slider = LUISliderWithLabel(filled=False, min_value=0.0, max_value=1.0, width=250.0, precision=4)
    slider2 = LUISliderWithLabel(filled=True, min_value=0.0, max_value=120.0, width=250.0, precision=1, value=32)
    bar = LUIProgressbar(width=250, value=33.5)

    btnOk = LUIButton(width=120, text=u"SUBMIT", template="ButtonMagic")
    btnCancel = LUIButton(width=120, text=u"CANCEL")
    btnCancel.right = 0

    picker = LUIColorpicker()
    pickLabel = LUILabel(text=u"Pick your favourite color", shadow=True)
    pickLabel.top = 6
    picker.right = 0

    box = LUISelectbox(width=250, options = [
            ("opt1", "Option 1"),
            ("opt2", "Option 2"),
            ("opt3", "Option 3"),
            ("opt4", "Option 4"),
            ("opt5", "Option 5"),
            ("opt6", "Option 6"),
            ("opt7", "Option 7"),
        ])

    def set_bar_value(parent, obj, val):
        bar.set_value(val)
        
    slider2.add_change_callback(set_bar_value)

    bar.set_value(slider2.get_value())

    field = LUIInputField(width=250)

    layout.add_row(checkbox)
    layout.add_row(checkboxChecked)
    layout.add_row(box)
    layout.add_row(radiobox)
    layout.add_row(radiobox2)
    layout.add_row(slider)
    layout.add_row(field)
    layout.add_row(slider2)
    layout.add_row(pickLabel, picker)
    layout.add_row(bar)
    layout.add_row(btnOk, btnCancel)
    layout.margin_top = 10

    instructions = LUIObject(region.root(), x=25, y=25) 

    # Title
    title = LUILabel(parent=instructions, text=u"LUI Basic Example", font_size=40, font="header")

    # Instructions
    layout = LUIVerticalLayout(parent=instructions, spacing=6)
    layout.add_row(LUILabel(text=u"Instructions:"))
    layout.add_row()
    layout.add_row(LUIKeyInstruction(key=u"A", instruction=u"Some fancy action"))
    layout.add_row(LUIKeyInstruction(key=u"Enter", instruction=u"Another action"))
    layout.top = 80

    skinParent.fit_to_children()

    bgFrame = LUISprite(region.root(), "blurred_background.jpg")
    bgFrame.bind("click", lambda event: bgFrame.request_focus())
    bgFrame.z_offset = -10
    # bgFrame.color = (0.1,0.1,0.1)
    bgFrame.centered = (True, True)

    base.accept("f3", region.toggle_render_wireframe)
    base.accept("f4", region.root().ls)
    base.run()

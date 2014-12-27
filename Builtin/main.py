
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
        win-fixed-size #t
    """)

    import direct.directbase.DirectStart

    LUIFontPool.get_global_ptr().register_font(
        "default", loader.loadFont("../Res/font/SourceSansPro-Semibold.ttf"))


    labelFont = loader.loadFont("../Res/font/SourceSansPro-Semibold.ttf")
    labelFont.setPixelsPerUnit(32)

    LUIFontPool.get_global_ptr().register_font(
        "label", labelFont)

    headerFont = loader.loadFont("../Res/font/SourceSansPro-Light.ttf")
    headerFont.setPixelsPerUnit(80)

    LUIFontPool.get_global_ptr().register_font(
        "header", headerFont)

    LUIAtlasPool.get_global_ptr().load_atlas(
        "skin", "res/atlas.txt", "res/atlas.png")

    base.win.set_clear_color(Vec4(0, 0, 0, 1))

    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    skinParent = LUIObject(region.root(),x=300,y=150,w=100,h=100)
    # skinParent.centered = (True, True)
    skinParent.top = 210
    skinParent.left = 20

    frame = UIFrame(parent=skinParent, width=300, height=370)
    layout = UIVerticalLayout(parent=frame.get_content_node(), width=250, spacing=10)   
    checkbox = UILabeledCheckbox(checked=False, text=u"Sample checkbox")
    checkboxChecked = UILabeledCheckbox(checked=True, text=u"Checked checkbox")

    group = UIRadioboxGroup()
    radiobox = UILabeledRadiobox(group=group, value=5, text=u"Radiobox")
    radiobox2 = UILabeledRadiobox(group=group, value=7, text=u"Radiobox Checked")

    radiobox2.get_box().set_active()

    slider = UISliderWithLabel(filled=False, min_value=0.0, max_value=1.0, width=250.0, precision=4)
    slider2 = UISliderWithLabel(filled=True, min_value=0.0, max_value=120.0, width=250.0, precision=1, value=32)
    bar = UIProgressbar(width=250, value=33.5)

    btnOk = UIButton(width=120, text=u"SUBMIT", template="ButtonMagic")
    btnCancel = UIButton(width=120, text=u"CANCEL")
    btnCancel.right = 0

    box = UISelectbox(width=250, options = [
            ("opt1", "Option 1"),
            ("opt2", "Option 2"),
            ("opt3", "Option 3"),
            ("opt4", "Option 4"),
            ("opt5", "Option 5"),
            ("opt6", "Option 6"),
            ("opt7", "Option 7"),
        ])

    def set_bar_value(obj, val):
        bar.set_value(val)
        
    slider2.add_change_callback(set_bar_value)

    bar.set_value(slider2.get_value())

    field = UIInputField(width=250)

    layout.add_row(checkbox)
    layout.add_row(checkboxChecked)
    layout.add_row(box)
    layout.add_row(radiobox)
    layout.add_row(radiobox2)
    layout.add_row(slider)
    layout.add_row(field)
    layout.add_row(slider2)
    layout.add_row(bar)
    layout.add_row(btnOk, btnCancel)

    instructions = LUIObject(region.root(), x=25, y=25) 

    # Title
    title = UILabel(parent=instructions, text=u"LUI Basic Example", font_size=40, font="header")

    # Instructions
    layout = UIVerticalLayout(parent=instructions, spacing=6)
    layout.add_row(UILabel(text=u"Instructions:"))
    layout.add_row()
    layout.add_row(UIKeyInstruction(key=u"A", instruction=u"Some fancy action"))
    layout.add_row(UIKeyInstruction(key=u"Enter", instruction=u"Another action"))
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

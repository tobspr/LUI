
if __name__ == "__main__":

    # Test script for This Skin
    from panda3d.core import *
    from Elements import *

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
    labelFont.setPixelsPerUnit(30)
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
    slider2 = UISliderWithLabel(filled=True, min_value=0.0, max_value=120.0, width=300.0, precision=1)
    bar = UIProgressbar(width=300, value=33.5)

    box = UISelectbox(width=300)

    def set_bar_value(obj, val):
        bar.set_value(val)
    slider2.add_change_callback(set_bar_value)
    bar.set_value(slider2.get_value())

    field = UIInputField(width=300)

    layout.add_column(checkbox)
    layout.add_column(radiobox)
    layout.add_column(radiobox2)
    layout.add_column(slider)
    layout.add_column(field)
    layout.add_column(slider2)
    layout.add_column(bar)
    layout.add_column(box)

    skinParent.fit_to_children()

    bgFrame = LUISprite(region.root(), "blank", "default", 0, 0, 10000, 10000)
    bgFrame.bind("click", lambda event: bgFrame.request_focus())
    bgFrame.z_offset = -1
    bgFrame.color = (0.1,0.1,0.1)
    base.accept("f3", region.toggle_render_wireframe)
    base.accept("f4", region.root().ls)
    base.run()

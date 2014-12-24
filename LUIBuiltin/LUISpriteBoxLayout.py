
from panda3d.lui import *

class LUISpriteBoxLayout(LUIObject):

    modes = ["tr", "top", "tl", "right", "mid", "left", "br", "bottom", "bl"]

    def __init__(self, image_prefix="", width=0, height=0):
        LUIObject.__init__(self, x=0, y=0, w=width, h=height)

        self.prefix = image_prefix
        self.parts = {}
        for i in self.modes:
            self.parts[i] = LUISprite(self, "blank", "default")
        self.render_layout()

    def render_layout(self):
        for i in self.modes:
            self.parts[i].set_texture(self.prefix + i, "default", resize=True)

        # Width
        self.parts['top'].width = self.width - self.parts['tl'].width - self.parts['tr'].width
        self.parts['mid'].width = self.width - self.parts['left'].width - self.parts['right'].width
        self.parts['bottom'].width = self.width - self.parts['bl'].width - self.parts['br'].width

        # Height
        self.parts['left'].height = self.height - self.parts['tl'].height - self.parts['bl'].height
        self.parts['mid'].height = self.height - self.parts['top'].height - self.parts['bottom'].height
        self.parts['right'].height = self.height - self.parts['tr'].height - self.parts['br'].height

        # Positioning - Left
        self.parts['top'].left = self.parts['tl'].width
        self.parts['mid'].left = self.parts['left'].width
        self.parts['bottom'].left = self.parts['bl'].width

        self.parts['tr'].left = self.parts['top'].left + self.parts['top'].width
        self.parts['right'].left = self.parts['mid'].left + self.parts['mid'].width
        self.parts['br'].left = self.parts['bottom'].left + self.parts['bottom'].width

        # Positioning - Top
        self.parts['left'].top = self.parts['tl'].height
        self.parts['mid'].top = self.parts['top'].height
        self.parts['right'].top = self.parts['tr'].height

        self.parts['bl'].top = self.parts['left'].top + self.parts['left'].height
        self.parts['bottom'].top = self.parts['mid'].top + self.parts['mid'].height
        self.parts['br'].top = self.parts['right'].top + self.parts['right'].height

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.render_layout()

    def on_mouseover(self, event):
        self.set_prefix("btn_hover/")

    def on_mouseout(self, event):
        self.set_prefix("btn_default/")


if __name__ == "__main__":

    # Test script for LUISpriteBoxLayout
    from panda3d.core import *

    load_prc_file_data("", """
        text-minfilter linear
        text-magfilter linear
        text-pixels-per-unit 32
        sync-video #f
        notify-level-lui debug
    """)
    import direct.directbase.DirectStart


    LUIFontPool.get_global_ptr().register_font(
        "default", loader.loadFont("../Res/font/SourceSansPro-Bold.ttf"))
    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Res/atlas.txt", "../Res/atlas.png")

    base.win.set_clear_color(Vec4(0.9, 0.9, 0.9, 1))
    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    layout = LUISpriteBoxLayout("btn_default/", 250, 250)
    layout.parent = region.root()
    layout.centered = (True, True)
    layout.color = (1, 1, 1)
    base.accept("f3", region.root().ls)
    run()

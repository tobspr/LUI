
from panda3d.lui import *

class SimpleSprite(LUIObject):

    def __init__(self):
        LUIObject.__init__(self, x=0, y=0, w=100, h=100)

        print "\n\nCreating demo sprite"
        self.someSprite = LUISprite(self, "blank", "default")

        print "\n\nSetting demo sprite position"
        self.someSprite.left = 10
        self.someSprite.top = 10

        print "\n\nSetting demo sprite size"
        self.someSprite.width = 222
        self.someSprite.height = 333


if __name__ == "__main__":

    # Test script for LUISpriteBoxLayout
    from panda3d.core import *

    load_prc_file_data("", """
        text-minfilter linear
        text-magfilter linear
        text-pixels-per-unit 32
        sync-video #f
        notify-level-lui spam
    """)
    import direct.directbase.DirectStart

    LUIFontPool.get_global_ptr().register_font(
        "default", loader.loadFont("../Res/font/SourceSansPro-Bold.ttf"))
    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Res/atlas.txt", "../Res/atlas.png")

    base.win.set_clear_color(Vec4(0.3, 0.3, 0.5, 1))
    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    print "\n\n\nCreating simple sprite"
    demo = SimpleSprite()

    print "\n\nPositioning sprite to root"
    demo.parent = region.root()
    # demo.centered = (True, True)
    # demo.color = (1, 1, 1)
    base.accept("f3", region.root().ls)
    # base.accept("f4", region.root().ls)
    run()
    # taskMgr.step()

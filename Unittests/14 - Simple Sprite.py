
from panda3d.lui import *

class SimpleSprite(LUIObject):

    def __init__(self):
        LUIObject.__init__(self, x=0, y=0, w=100, h=100)
        self.someSprite = LUISprite(self, "blank", "default")
        self.someSprite.left = 10
        self.someSprite.top = 10
        self.someSprite.width = 222
        self.someSprite.height = 333
        self.anotherSpriteContainer = LUIObject(self, x=100, y=100, w=100, h=100)
        self.anotherSprite = LUISprite(self.anotherSpriteContainer, "blank", "default")
        self.anotherSprite.size = (100, 100)
        self.anotherSprite.pos = (1, 1)
        self.anotherSprite.color = (0.2, 0.6, 1.0)


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
        "default", loader.loadFont("../Builtin/font/SourceSansPro-Bold.ttf"))
    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Builtin/res/atlas.txt", "../Builtin/res/atlas.png")

    base.win.set_clear_color(Vec4(0.3, 0.3, 0.5, 1))
    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)
    demo = SimpleSprite()

    print "\n\nSetting parent"
    demo.parent = region.root()

    print "\n\nResetting parent"
    # region.root().remove_all_children()

    print "\n\nSetting parent"
    demo.parent = region.root()


    print "\n\n\nForcing recompute"
    demo.anotherSprite.pos = (10, 10)

    print "\n\nRun one frame"
    # demo.parent = region.root()
    # demo.centered = (True, True)
    # demo.color = (1, 1, 1)
    base.accept("f3", region.root().ls)
    # base.accept("f4", region.root().ls)
    # run()
    taskMgr.step()

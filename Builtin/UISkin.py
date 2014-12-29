

from panda3d.lui import LUIFontPool, LUIAtlasPool
from panda3d.core import Filename
from os.path import join

class UISkin:

    skinLocation = ""

    def __init__(self):
        pass

    def load(self):
        pass

    def get_resource(self, pth):
        return Filename.from_os_specific(join(self.skinLocation, pth)).get_fullpath()


class UIDefaultSkin(UISkin):

    skinLocation = "E:/Projects/Brainz stuff/LUI/Builtin"
    # skinLocation = "."

    def __init__(self):
        pass

    def load(self):
        LUIFontPool.get_global_ptr().register_font(
            "default", loader.loadFont(self.get_resource("font/SourceSansPro-Semibold.ttf")))

        labelFont = loader.loadFont(self.get_resource("font/SourceSansPro-Semibold.ttf"))
        labelFont.setPixelsPerUnit(32)

        LUIFontPool.get_global_ptr().register_font(
            "label", labelFont)

        headerFont = loader.loadFont(self.get_resource("font/SourceSansPro-Light.ttf"))
        headerFont.setPixelsPerUnit(80)

        LUIFontPool.get_global_ptr().register_font("header", headerFont)

        LUIAtlasPool.get_global_ptr().load_atlas("skin", 
            join(self.skinLocation, "res/atlas.txt"), 
            self.get_resource("res/atlas.png"))


from panda3d.lui import LUIFontPool, LUIAtlasPool
from panda3d.core import Filename
import os
from os.path import join

from LUISkin import LUISkin
from LUILabel import LUILabel

class LUIMetroSkin(LUISkin):

    """ Simple Metro / Flat UI skin """

    skin_location = os.path.dirname(os.path.abspath(__file__))

    def load(self):
        LUIFontPool.get_global_ptr().register_font(
            "default", loader.loadFont(self.get_resource("font/Roboto-Medium.ttf")))

        label_font = loader.loadFont(self.get_resource("font/Roboto-Medium.ttf"))
        label_font.set_pixels_per_unit(32)
        LUIFontPool.get_global_ptr().register_font("label", label_font)

        headerFont = loader.loadFont(self.get_resource("font/Roboto-Light.ttf"))
        headerFont.set_pixels_per_unit(80)

        LUIFontPool.get_global_ptr().register_font("header", headerFont)

        LUIAtlasPool.get_global_ptr().load_atlas("skin",
            self.get_resource("res/atlas.txt"),
            self.get_resource("res/atlas.png"))

        # Label color
        # LUILabel.DEFAULT_COLOR = (0.0, 0.0, 0.0, 0.6)
        # LUILabel.DEFAULT_USE_SHADOW = False

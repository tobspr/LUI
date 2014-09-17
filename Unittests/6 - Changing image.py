
import sys

sys.path.insert(0, "../")

from panda3d.lui import *
from panda3d.core import loadPrcFileData, TexturePool, LVector2, LTexCoord

loadPrcFileData("", "notify-level-lui spam")


class BasicButton(LUIObject):

    def __init__(self, text):
        LUIObject.__init__(self, x=0, y=0, w=50, h=30)

    def test(self):
        
        print "\nSetting inital image"
        sprite = self.attach_sprite("../Res/atlas.png")

        print "\nChanging image"
        sprite.set_texture("../Res/btn_left.png")

        print "\nChanging image"
        sprite.set_texture("../Res/btn_mid.png")

        print "\nChanging image"
        sprite.set_texture("../Res/btn_right.png")

        print "\nAttaching new sprite with the same image"
        sprite2 = self.attach_sprite("../Res/btn_right.png")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

root = LUIRoot(512,512)

button = BasicButton("Hello")
button.set_top_left(20, 20)

print "\n\nAttaching button:"
root.node().add_child(button)

print "\n\nTesting .."
button.test()

print "\n\nListing scene graph .."

root.node().ls()
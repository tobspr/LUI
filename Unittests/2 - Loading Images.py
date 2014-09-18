
import sys

sys.path.insert(0, "../")

from panda3d.lui import *

from panda3d.core import loadPrcFileData, TexturePool, LVector2, LTexCoord

loadPrcFileData("", "notify-level-lui debug")


class BasicButton(LUIObject):

    def __init__(self, text):
        LUIObject.__init__(self, 50, 30)

        print "\nTest case 1: Setting & Getting size"
        print self.get_size()
        self.set_size(100, 200)
        print self.get_size()

        print "\nTest case 2: Using 'default:image'"
        self.imgMid = LUISprite(self, "btn_mid", "default")

        print "\nTest case 3: Attaching an arbitrary image"
        self.imgRight3 = LUISprite(self, "../Res/btn_mid.png", 32, 32)

        print "\nTest case 4: Attaching a texture object"
        self.imgRight4 = LUISprite(self, 
            TexturePool.loadTexture("../Res/btn_right.png"))

        print "\nTest case 5: Attaching a non-existing image"
        self.imgRight5 = LUISprite(self, "Res/DoesNotExist.png")

        print "\nTest case 6: Attaching a sprite, but not storing a reference"
        LUISprite(self, "btn_right", "default")

        print "\nTest case 7: Attaching and instantly removing a sprite"
        tmp = LUISprite(self, "btn_right", "default")
        self.remove_child(tmp)

        print "\nTest case 8: Resizing widget"
        self.set_size(30, 40)

        print "\nTest case 9: Positioning widget"
        self.set_pos(50, 50)

        print "\nTesting if all pointers are still valid"

        for sprite in self.children:
            start = LTexCoord()
            end = LTexCoord()
            sprite.get_uv_range(start, end)
            sprite.print_vertices()

        print "Test passed."

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

root = LUIRoot(512, 512)
# root.load_atlas("default")
# root.reparent_to(pixel2d)

button = BasicButton("Hello")
button.set_top_left(20, 20)

print "\n\nAttaching button:"
root.node().add_child(button)
# button.bind("click", myClickHandler)
# root += button

print "\n\nListing scene graph .."

root.node().ls()


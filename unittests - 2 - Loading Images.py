
import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIRoot, LUIAtlasPool

from panda3d.core import loadPrcFileData, TexturePool, LVector2, LTexCoord

# loadPrcFileData("", "notify-level-lui spam")


class BasicButton(LUINode):

    def __init__(self, text):
        LUINode.__init__(self, 50, 30)

        print "\nTest case 1: Setting & Getting size"
        print self.get_size()
        self.set_size(100, 200)
        print self.get_size()

        print "\nTest case 2: Using 'default:image'"
        self.imgMid = self.attach_sprite("btn_mid", "default")

        print "\nTest case 3: Attaching an arbitrary image"
        self.imgRight3 = self.attach_sprite("Res/atlas.png", 32, 32)

        print "\nTest case 4: Attaching a texture object"
        self.imgRight4 = self.attach_sprite(
            TexturePool.loadTexture("Res/atlas.png"))

        print "\nTest case 5: Attaching a non-existing image"
        self.imgRight5 = self.attach_sprite("Res/DoesNotExist.png")

        print "\nTest case 6: Attaching a sprite, but not storing a reference"
        self.attach_sprite("btn_right", "default")

        print "\nTest case 7: Attaching and instantly removing a sprite"
        tmp = self.attach_sprite("btn_right", "default")
        self.remove_sprite(tmp)

        print "\nTest case 8: Resizing widget"
        self.set_size(30, 40)

        print "\nTest case 9: Positioning widget"
        self.set_pos(50, 50)

        print "\nTesting if all pointers are still valid"
        print "Num attached sprites: ", self.get_sprite_count()

        for n in xrange(self.get_sprite_count()):
            sprite = self.get_sprite(n)

            start = LTexCoord()
            end = LTexCoord()
            sprite.get_uv_range(start, end)

            print "\tSprite:"
            print "\t\tAbs-Pos:", sprite.get_abs_pos()
            print "\t\tSize:", sprite.get_size()
            print "\t\tTexcoord:", start, ",", end

        print "Test passed."

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

root = LUIRoot()
# root.load_atlas("default")
# root.reparent_to(pixel2d)

button = BasicButton("Hello")
button.set_top_left(20, 20)
# button.bind("click", myClickHandler)
# root += button

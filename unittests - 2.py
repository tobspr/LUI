
import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIRoot, LUIAtlasPool

from panda3d.core import loadPrcFileData, TexturePool, LVector2

# loadPrcFileData("", "notify-level-lui spam")


class BasicButton(LUINode):

    """ This is a builting template. It will be included with LUI. """

    def __init__(self, text):
        LUINode.__init__(self, 50, 30)


        print "\nTest case 1: Setting & Getting size"
        print self.get_size()
        self.set_size(100, 200)
        print self.get_size()


        print "\nTest case 1: Using ':image'"
        self.imgLeft = self.attach_sprite(0, 0, ":btn_left")

        print "\nTest case 2: Using 'default:image'"
        self.imgMid = self.attach_sprite(10, 0, "default:btn_mid")

        print "\nTest case 3: Using get_atlas_image('image')"
        self.imgRight = self.attach_sprite(
            50, 0, self.get_atlas_image("btn_right"))

        print "\nTest case 4: Using get_atlas_image('default', 'image')"
        self.imgRight2 = self.attach_sprite(
            50, 0, self.get_atlas_image("default", "btn_right"))


        print "\nTest case 5: Attaching an arbitrary image"
        self.imgRight3 = self.attach_sprite(
            50, 0, "Res/atlas.png")

        print "\nTest case 6: Attaching a texture object"
        self.imgRight4 = self.attach_sprite(
            50, 0, TexturePool.loadTexture("Res/atlas.png"))

        print "\nTest case 7: Attaching a non-existing image"
        self.imgRight5 = self.attach_sprite(
            50, 0, "Res/DoesNotExist.png")

        print "\nTest case 8: Attaching a sprite, but not storing a reference"
        self.attach_sprite(50, 0, ":btn_right")

        print "\nTest case 9: Attaching and instantly removing a sprite"
        tmp = self.attach_sprite(0, 0, ":btn_right")
        self.remove_sprite(tmp)

        print "\nTesting if all pointers are still valid"
        print "Num attached sprites: ", self.get_sprite_count()

        for n in xrange(self.get_sprite_count()):
            sprite = self.get_sprite(n)
            print "\tSprite:"
            print "\t\tSize:", sprite.get_size()
            print "\t\tTexc-Start:", sprite.get_texcoord_start()
            print "\t\tTexc-End:", sprite.get_texcoord_end()

        print "\nTest case 10: Resizing widget"
        self.set_size(30, 40)
        

    def on_mouse_over(self, event):
        self.imgLeft.set_texture(":btn_left_hover")
        self.imgMid.set_texture(":btn_mid_hover")
        self.imgRight.set_texture(":btn_right_hover")

    def on_mouse_out(self, event):
        self.imgLeft.set_texture(":btn_left")
        self.imgMid.set_texture(":btn_mid")
        self.imgRight.set_texture(":btn_right")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

root = LUIRoot()
# root.load_atlas("default")
# root.reparent_to(pixel2d)

button = BasicButton("Hello")
button.set_pos(20, 20)
button.bind("click", myClickHandler)
root += button


import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIRoot


class BasicButton(LUINode):

    """ This is a builting template. It will be included with LUI. """

    def __init__(self, text):
        LUINode.__init__(self)

        self.imgLeft = self.attach_sprite(
            00, 0, self.get_atlas_image("default", "btn_left"))
        self.imgMid = self.attach_sprite(
            10, 0, self.get_atlas_image("default", "btn_mid"))
        self.imgRight = self.attach_sprite(
            50, 0, self.get_atlas_image("default", "btn_right"))
        self.text = self.attach_text(0, 0, text, 20, TextNode.ACenter, 50)

        self.bind("mouseover", self.on_mouse_over)
        self.bind("mouseout", self.on_mouse_out)

        self.imgRight = self.attach_sprite(
            50, 0, loader.loadTexture("btn_right"))

    def on_mouse_over(self, event):
        self.imgLeft.set_texture(
            self.get_atlas_image("default", "btn_left_hover"))
        self.imgMid.set_texture(
            self.get_atlas_image("default", "btn_mid_hover"))
        self.imgRight.set_texture(
            self.get_atlas_image("default", "btn_right_hover"))

    def on_mouse_out(self, event):
        self.imgLeft.set_texture(self.get_atlas_image("btn_left"))
        self.imgMid.set_texture(self.get_atlas_image("btn_mid"))
        self.imgRight.set_texture(self.get_atlas_image("btn_right"))

root = LUIRoot()
root.reparent_to(pixel2d)
root.load_atlas("default", "atlas.dat", "atlas.png")

button = BasicButton()
button.set_pos(20, 20)
button.bind("click", myClickHandler)
root += button

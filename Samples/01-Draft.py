
from LUI import LUINode

class BasicButton(LUINode):

    def __init__(self, text):
        LUINode.__init__(self)

        self.imgLeft  = self.attach_sprite(00, 0, self.get_atlas_image("btn_left.png"))
        self.imgMid   = self.attach_sprite(10, 0, self.get_atlas_image("btn_mid.png"))
        self.imgRight = self.attach_sprite(50, 0, self.get_atlas_image("btn_right.png"))
        self.text     = self.attach_text(0, 0, text, 20, TextNode.ACenter, 50)

        self.bind("mouseover", self.on_mouse_over)
        self.bind("mouseout", self.on_mouse_out)

    def on_mouse_over(self, event):
        self.imgLeft.set_texture(self.get_atlas_image("btn_left_hover.png"))
        self.imgMid.set_texture(self.get_atlas_image("btn_mid_hover.png"))
        self.imgRight.set_texture(self.get_atlas_image("btn_right_hover.png"))
        
    def on_mouse_out(self, event):
        self.imgLeft.set_texture(self.get_atlas_image("btn_left.png"))
        self.imgMid.set_texture(self.get_atlas_image("btn_mid.png"))
        self.imgRight.set_texture(self.get_atlas_image("btn_right.png"))

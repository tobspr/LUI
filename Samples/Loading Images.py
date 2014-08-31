
from LUI import LUINode
from panda3d.core import TexturePool

class TestLUINode(LUINode):

    def __init__(self):

        # This loads the sprite "btn_left" from the atlas "default"
        self.attach_sprite(":btn_left")
        self.attach_sprite("default:btn_left")
        self.attach_sprite(self.get_atlas_image("btn_left"))
        self.attach_sprite(self.get_atlas_image("default", "btn_left"))

        # This loads the sprite "btn_left" from the atlas "myAtlas"
        self.attach_sprite("myAtlas:btn_left")
        self.attach_sprite(self.get_atlas_image("myAtlas", "btn_left"))

        # This loads the sprite my_image.png from disk
        self.attach_sprite("my_image.png")

        # This also loads the sprite my_image.png, but from an existing texture
        self.attach_sprite(TexturePool.loadTexture("my_image.png"))

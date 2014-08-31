
from LUI import LUINode, LUIRoot
from panda3d.core import TexturePool


class TestLUINode(LUINode):

    def __init__(self):

        LUINode.__init__(self)

        # This loads the sprite "btn_left" from the atlas "default"
        self.attach_sprite("btn_left", "default")

        # This loads the sprite "btn_left" from the atlas "myAtlas"
        self.attach_sprite("btn_left", "myAtlas")

        # This loads the sprite my_image.png from disk
        self.attach_sprite("my_image.png")

        # This also loads the sprite my_image.png, but from an existing texture
        self.attach_sprite(TexturePool.loadTexture("my_image.png"))

        # You can also pass a x/y position when calling attach_sprite, this is
        # equal to creating the sprite and then calling set_top_left, e.g:
        self.attach_sprite("myAtlas", "btn_left", 10, 10)

LUIRoot().root().attach_sprite("btn_left.png")



from panda3d.lui import *


class LUIButton(LUIObject):

    def __init__(self, text="Hello", width=100):
        LUIObject.__init__(self, x=0, y=0, w=width, h=50)

        self.sprite_left = LUISprite(self, "btn_left", "default")
        self.sprite_mid = LUISprite(self, "btn_mid", "default")
        self.sprite_right = LUISprite(self, "btn_right", "default")

        self.sprite_mid.set_width(
            width - self.sprite_left.get_width() - self.sprite_right.get_width())
        self.sprite_mid.set_left(self.sprite_left.get_width())

        self.sprite_right.set_left(
            self.sprite_mid.get_left() + self.sprite_mid.get_width())

        self.set_height(self.sprite_mid.get_height())

        self.text = LUIText(self, text, "default", 16.0)
        self.text.set_centered()
        self.text.set_relative_z_index(100)

        self.sprite_left.left = 10.0


        self.bind("mouseover", self.handle_event)
        self.bind("mouseout", self.handle_event)
        self.bind("mousedown", self.handle_event)
        self.bind("mouseup", self.handle_event)
        self.bind("click", self.on_click)

    def on_click(self, event):
        print "on click!"

    def handle_event(self, event):

        if event.get_name() == "mouseover":
            for child in [self.sprite_left, self.sprite_mid, self.sprite_right]:
                child.set_alpha(0.99)
        elif event.get_name() == "mouseout":
            for child in [self.sprite_left, self.sprite_mid, self.sprite_right]:
                child.set_alpha(1.0)
        elif event.get_name() == "mousedown":
            self.sprite_left.set_texture("btn_active_left", "default", resize=False)
            self.sprite_right.set_texture("btn_active_right", "default", resize=False)
            self.sprite_mid.set_texture("btn_active_mid", "default", resize=False)
            self.text.set_margin_top(1.0)
        elif event.get_name() == "mouseup":
            self.sprite_left.set_texture("btn_left", "default", resize=False)
            self.sprite_right.set_texture("btn_right", "default", resize=False)
            self.sprite_mid.set_texture("btn_mid", "default", resize=False)
            self.text.set_margin_top(0.0)


if __name__ == "__main__":

    # Test script for LUIButton
    from panda3d.core import *

    load_prc_file_data("", """

        text-minfilter linear
        text-magfilter linear
        notify-level-lui debug

    """)
    import direct.directbase.DirectStart

    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Res/atlas.txt", "../Res/atlas.png")

    base.win.set_clear_color(Vec4(0.5,0.5,0.5,1))

    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    button = LUIButton("Click Me")
    button.set_centered()
    region.root().add_child(button)


    base.accept("f3", region.root().ls)

    run()

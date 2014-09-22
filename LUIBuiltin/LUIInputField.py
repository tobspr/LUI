

from panda3d.lui import *


class LUIInputField(LUIObject):

    def __init__(self, width=200, font_size=20):
        LUIObject.__init__(self, x=0, y=0, w=width, h=font_size+10)

        self.background = LUISprite(
            self, "blank", "default", 0, 0, width, font_size + 10, (0.95, 0.95, 0.95, 1.0))
        self.background.z_offset = 5

        self.background_border = LUISprite(
            self, "blank", "default", -1, -1, width + 2, font_size + 12, (0.2, 0.6, 1.0, 1.0))

        self.text_clip = LUIObject(parent=self, x=0, y=0,w=width,h=font_size+10)
        self.text_clip.clip_bounds = (5, 5, 5, 5)

        self.text = LUIText(self.text_clip, u"", "default", font_size)
        self.text.color = (0.5, 0.5, 0.5)
        self.text.margin.top = 3
        self.text.margin.left = 3
        self.text.z_offset = 10

        self.cursor = LUISprite(
            self, "blank", "default", x=0, y=0, w=2, h=font_size)
        self.cursor.color = (0.2, 0.2, 0.2)
        self.cursor.margin = (6, 0, 0, 2)
        self.cursor.z_offset = 20

        self.background_border.hide()
        self.cursor.hide()

        self._current_text = u""
        self._place_cursor()

        self.background.debug_name = "Background"
        self.background_border.debug_name = "BG_border"
        self.debug_name = "LUIInputField"
        self.text.debug_name = "InputText"
        self.cursor.debug_name = "Cursor"
        self.text_clip.debug_name = "TextClip"

    def _render_text(self):
        self.text.text = self._current_text
        self._place_cursor()

    def _add_text(self, text):
        self._current_text += text
        self._render_text()

    def on_click(self, event):
        self.request_focus()

    def on_focus(self, event):
        print "Got focus .."
        self.background_border.show()
        self.cursor.show()

    def on_keydown(self, event):
        key_name = event.get_message()
        if key_name == "backspace":
            self._current_text = self._current_text[:-1]
            self._render_text()
        # elif key_name == "space":
        #     self._add_text(" ")

    def on_keyrepeat(self, event):
        self.on_keydown(event)

    def on_textinput(self, event):
        print "On textinput .."
        self._add_text(event.get_message())

    def on_blur(self, event):
        print "Lost focus .."
        self.background_border.hide()
        self.cursor.hide()

    def _place_cursor(self):
        self.cursor.left = self.text.left + self.text.width

if __name__ == "__main__":

    # Test script for LUIInputField
    from panda3d.core import *

    load_prc_file_data("", """

        text-minfilter linear
        text-magfilter linear
        notify-level-lui debug
        text-pixels-per-unit 32
        sync-video #f

    """)
    import direct.directbase.DirectStart

    LUIFontPool.get_global_ptr().register_font(
        "default", loader.loadFont("../Res/font/SourceSansPro-Semibold.ttf"))
    LUIAtlasPool.get_global_ptr().load_atlas(
        "default", "../Res/atlas.txt", "../Res/atlas.png")

    base.win.set_clear_color(Vec4(1, 0, 0, 1))

    region = LUIRegion.make("LUI", base.win)
    handler = LUIInputHandler()
    base.mouseWatcher.attach_new_node(handler)
    region.set_input_handler(handler)

    bgFrame = LUISprite(region.root(), "blank", "default", 0, 0, 10000, 10000)
    bgFrame.bind("click", lambda event: bgFrame.request_focus())
    bgFrame.z_offset = -1

    inputfield = LUIInputField(width=300, font_size=15)
    inputfield.parent = region.root()

    inputfield.centered = (True, True)

    # base.accept("f3", region.root().ls)
    base.accept("f3", region.toggle_render_wireframe)

    print "Root is at ", region.root()

    base.run()

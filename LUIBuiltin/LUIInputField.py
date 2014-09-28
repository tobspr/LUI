

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
        self.text_clip.clip_bounds = (2, 2, 2, 2)

        self.text_scroller = LUIObject(parent=self.text_clip, x=0, y=0)

        self.text = LUIText(self.text_scroller, u"", "default", font_size)
        self.text.color = (0.5, 0.5, 0.5)
        self.text.margin_top = 3
        self.text.margin_left = 3
        self.text.z_offset = 10

        self.cursor = LUISprite(
            self.text_scroller, "blank", "default", x=0, y=0, w=2, h=font_size)
        self.cursor.color = (0.2, 0.2, 0.2)
        self.cursor.margin = (6, 0, 0, 0)
        self.cursor.z_offset = 20

        self.cursor_index = 0

        self.background_border.hide()
        self.cursor.hide()

        self.current_text = u""
        self.render_text()

    def render_text(self):
        self.text.text = self.current_text
        self.cursor.left = self.text.left + self.text.get_char_pos(self.cursor_index)

        max_left = self.width - 5

        # Scroll if the cursor is outside of the clip bounds

        relX = self.get_relative_pos(self.cursor.get_abs_pos()).x
        if relX >= max_left:
            self.text_scroller.left = min(0, max_left - self.cursor.left)
        if relX <= 0:
            self.text_scroller.left = min(0, - self.cursor.left - relX)

    def set_cursor_pos(self, pos):
        self.cursor_index = max(0, min(len(self.current_text), pos))

    def add_text(self, text):
        self.current_text = self.current_text[:self.cursor_index] + text + self.current_text[self.cursor_index:]
        self.set_cursor_pos(self.cursor_index + len(text))
        self.render_text()

    def on_click(self, event):
        self.request_focus()

    def on_mousedown(self, event):
        local_x_offset = self.text.get_relative_pos(event.coordinates).x
        self.set_cursor_pos(self.text.get_char_index(local_x_offset))
        self.render_text()

    def on_focus(self, event):
        self.background_border.show()
        self.cursor.show()

    def on_keydown(self, event):
        key_name = event.get_message()
        if key_name == "backspace":
            self.current_text = self.current_text[:max(0, self.cursor_index - 1)] + self.current_text[self.cursor_index:]
            self.set_cursor_pos(self.cursor_index - 1)
            self.render_text()
        elif key_name == "delete":
            self.current_text = self.current_text[:self.cursor_index] + self.current_text[min(len(self.current_text), self.cursor_index + 1):]
            self.set_cursor_pos(self.cursor_index)
            self.render_text()
        elif key_name == "arrow_left":
            self.set_cursor_pos(self.cursor_index - 1)
            self.render_text()
        elif key_name == "arrow_right":
            self.set_cursor_pos(self.cursor_index + 1)
            self.render_text()

    def on_keyrepeat(self, event):
        self.on_keydown(event)

    def on_textinput(self, event):
        self.add_text(event.get_message())

    def on_blur(self, event):
        self.background_border.hide()
        self.cursor.hide()


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

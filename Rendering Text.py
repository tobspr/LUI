
import sys

sys.path.insert(0, "../")

from panda3d.core import *
# from panda3d.lui import *

# loadPrcFileData("", "notify-level-lui spam")
# loadPrcFileData("", "notify-level spam")
loadPrcFileData("", "show-frame-rate-meter #t")


# LUIAtlasPool.get_global_ptr().load_atlas(
#     "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

testStr = "Hello World - abcdefghijklmnopqrstuvwxyz 1^"

textMaker = PNMTextMaker("Res/font/SourceSansPro-Semibold.ttf", 0)

ps = 30
textMaker.set_pixel_size(ps)
textMaker.set_native_antialias(True)

w = textMaker.calc_width(testStr)
h = int(textMaker.get_line_height() * ps)

c = CardMaker("a")
c.set_frame(0, w, 0, h)
cn = pixel2d.attach_new_node(c.generate())
cn.set_pos(10, 0, -300)

s = PNMImage(w, h)
s.fill(0.2, 0.6, 1.0)
textMaker.generate_into(testStr, s, 0, ps)

t = Texture()
t.load(s)
cn.set_texture(t)
cn.set_transparency(TransparencyAttrib.MAlpha)

# t.load(s)

base.run()

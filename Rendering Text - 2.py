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

font = TextProperties.get_default_font()

ps = 100
font.set_pixel_size(ps)
font.set_pixels_per_unit(100)
font.set_native_antialias(True)

g = font.get_glyph(ord('W'))

c = CardMaker("a")
c.set_frame(0, 100, 0, 100)
c.set_uv_range(Point2(g.get_uv_left(), g.get_uv_bottom()), Point2(g.get_uv_right(), g.get_uv_top()))
cn = pixel2d.attach_new_node(c.generate())
cn.set_pos(10, 0, -300)

cn.set_texture(g.get_page())
cn.set_transparency(TransparencyAttrib.MAlpha)

base.run()

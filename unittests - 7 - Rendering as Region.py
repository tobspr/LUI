
import sys

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

loadPrcFileData("", "notify-level-lui spam")
# loadPrcFileData("", "notify-level spam")
loadPrcFileData("", "show-frame-rate-meter #f")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)
# region.set_active(1)

for i in xrange(1):
    # sprite = region.root().attach_sprite("Res/demo_textures/" + str(i) + ".png")
    # sprite = region.root().attach_sprite("btn_left", "default")
    # sprite.set_size(64, 64)
    # sprite.set_pos(20, 20)
    # sprite.set_left(50)
    # sprite.set_top(50)

    btn = LUIObject(110, 100)
    region.root().add_child(btn)
    btn.set_pos(100, 100)
    sprite_left = btn.attach_sprite("btn_left", "default")
    sprite_mid = btn.attach_sprite("btn_mid", "default")
    sprite_mid.set_left(sprite_left.get_width())
    sprite_mid.set_width(100)
    sprite_right = btn.attach_sprite("btn_right", "default")
    sprite_right.set_left(sprite_left.get_width() + sprite_mid.get_width())

    btn.set_right(20)
    btn.set_bottom(20)
    btn.set_height(sprite_mid.get_height())

    def test():
        # btn.remove_sprite(sprite_mid)
        sprite_mid.hide()

    base.accept("f4", test)
    # sprite.set_uv_range(0.0, 1.0, 1.0, 0.5)
    # sprite.set_color(0.0, 1.0, 0.0, 0.1)
    # sprite.set_pos(-0.5 + xoffs, -0.5 + yoffs)
    # sprite.set_size(200, 200)

region.root().ls()

base.run()

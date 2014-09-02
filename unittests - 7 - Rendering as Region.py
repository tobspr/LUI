
import sys

sys.path.insert(0, "../")

from panda3d.core import *
from LUI import *

loadPrcFileData("", "notify-level-lui fatal")
loadPrcFileData("", "notify-level-glgsg spam")
loadPrcFileData("", "show-frame-rate-meter #t")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)
region.set_active(1)

for i in xrange(1):
    sprite = region.root().attach_sprite("Res/demo_textures/" + str(i) + ".png")
    xoffs = int(i % 8) / 8.0
    yoffs = int(i / 8) / 8.0
    sprite.set_size(100, 100)
    sprite.set_pos(-0.5 + xoffs, -0.5 + yoffs)



base.run()


import sys

sys.path.insert(0, "../")

from panda3d.core import *
from LUI import *

loadPrcFileData("", "notify-level-lui spam")
loadPrcFileData("", "show-frame-rate-meter #t")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")


import direct.directbase.DirectStart
region = LUIRegion.make("LUI", base.win)
region.set_active(1)


sprite = region.root().attach_sprite("Res/btn_left.png")
sprite.set_size(0.1, 0.1)
sprite.set_pos(0.5, -0.5)

run()

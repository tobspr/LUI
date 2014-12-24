
import sys
import time

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

# loadPrcFileData("", "notify-level-lui spam")
loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")


loadPrcFileData("", "framebuffer-multisample #t")
loadPrcFileData("", "multisamples 16")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)
parent = region.root()
parent.z_offset = 100

sprite1 = LUISprite(parent, "blank", "default", x=100, y=100, w=100, h=100)
sprite2 = LUISprite(parent, "blank", "default", x=150, y=120, w=100, h=100)
sprite3 = LUISprite(parent, "blank", "default", x=125, y=150, w=100, h=100)

sprite1.set_color(0.2, 0.0, 0.0, 0.5)
sprite2.set_color(0.4, 0.0, 0.0, 0.5)
sprite3.set_color(0.6, 0.0, 0.0, 0.5)

sprite1.z_offset = 1
sprite2.z_offset = 2
sprite3.z_offset = 3



run()

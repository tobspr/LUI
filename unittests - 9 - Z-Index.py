
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
    "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)
parent = region.root()
parent.set_relative_z_index(100)

sprite1 = parent.attach_sprite("blank", "default", x=100, y=100, w=100, h=100)
sprite2 = parent.attach_sprite("blank", "default", x=150, y=120, w=100, h=100)
sprite3 = parent.attach_sprite("blank", "default", x=125, y=150, w=100, h=100)

sprite1.set_color(0.2,0.6,1.0, 0.5)
sprite2.set_color(0.4,0.6,1.0, 0.5)
sprite3.set_color(0.6,0.6,1.0, 0.5)

sprite1.set_relative_z_index(1)
sprite2.set_relative_z_index(4)
sprite3.set_relative_z_index(3)

parent.ls()

run()
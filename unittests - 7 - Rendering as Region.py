
import sys

sys.path.insert(0, "../")

from panda3d.core import *
from LUI import *

loadPrcFileData("", "notify-level-lui spam")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")


import direct.directbase.DirectStart
region = LUIRegion.make("LUI", base.win)
region.set_active(1)
run()

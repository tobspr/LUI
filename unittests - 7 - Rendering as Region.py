
import sys

sys.path.insert(0, "../")

from LUI import LUIObject, LUIRoot, LUIAtlasPool, LUIRegion
from panda3d.core import *

loadPrcFileData("", "notify-level-lui spam")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

# root = LUIRoot(512,512)

print [k for k in dir(LUIRegion) if k.startswith("m")]

import direct.directbase.DirectStart
region = LUIRegion.make("LUI", base.win)

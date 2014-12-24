# -*- encoding: UTF-8 -*-
import sys
sys.path.insert(0, "../")
import random
from panda3d.core import *
# from panda3d.lui import *
loadPrcFileData("", "notify-level-lui spam")
# loadPrcFileData("", "notify-level spam")

loadPrcFileData("", "text-pixels-per-unit 100")
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "text-minfilter linear")
loadPrcFileData("", "text-magfilter linear")
loadPrcFileData("", "depth-bits 32")
loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "text-page-size 256 256")
loadPrcFileData("", "win-size 500 500")

import direct.directbase.DirectStart

import math

from panda3d.lui import *

fontPool = LUIFontPool.get_global_ptr()
luiRegion = LUIRegion.make("test", base.win)
luiTop = luiRegion.root()

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

luiRegion.root().clip_bounds = (100, 100, 100, 100)

LUISprite(luiRegion.root(), "blank", "default", 0, 0, 2000, 2000)

base.run()
taskMgr.step()

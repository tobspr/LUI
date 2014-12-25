# -*- encoding: UTF-8 -*-
import sys
import os
sys.path.insert(0, "../")
import random
from panda3d.core import *
# from panda3d.lui import *
# loadPrcFileData("", "notify-level-lui spam")
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

# luiRegion.root().clip_bounds = (100, 100, 100, 100)

s1 = LUIObject(luiRegion.root(), 0, 0, 200, 200)
s1.clip_bounds = (0,0,0,0)
s1.centered = (True, True)

showBounds = LUISprite(luiRegion.root(), "blank", "default", 0, 0, 10, 10)
showBounds.color = (0.2,0.6,1.0,0.3)
showBounds.z_offset = 100

# s3 = LUIObject(s1, 10, 10, 200, 200)
# s3.clip_bounds = (0,0,0,0)

s2 = LUISprite(s1, "blank", "default", -1000, -1000, 2000, 2000)
s2.color = (1.0,0.6,0.2)

def test(task):
    os.system("cls")
    print "\n\nBOUNDS = ",
    print s2.get_abs_clip_bounds().x
    print s2.get_abs_clip_bounds().y
    print s2.get_abs_clip_bounds().w
    print s2.get_abs_clip_bounds().h

    # showBounds.left = s2.get_abs_clip_bounds().x
    # showBounds.top = s2.get_abs_clip_bounds().y
    # showBounds.width = s2.get_abs_clip_bounds().w
    # showBounds.height = s2.get_abs_clip_bounds().h

    showBounds.left = s1.left
    showBounds.top = s1.top
    showBounds.width = s1.width
    showBounds.height = s1.height



    return task.cont
base.addTask(test, "test")

base.run()
# taskMgr.step()

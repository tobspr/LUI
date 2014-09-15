# -*- encoding: UTF-8 -*-
import sys
sys.path.insert(0, "../")
import random
from panda3d.core import *
# from panda3d.lui import *
# loadPrcFileData("", "notify-level-lui spam")
# loadPrcFileData("", "notify-level spam")

loadPrcFileData("", "text-pixels-per-unit 50")
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "text-minfilter linear")
loadPrcFileData("", "text-magfilter linear")
loadPrcFileData("", "sync-video #f")
# loadPrcFileData("", "text-scale-factor 1.0")
loadPrcFileData("", "text-page-size 256 256")
loadPrcFileData("", "framebuffer-multisample #t")
loadPrcFileData("", "multisamples 16")
# LUIAtlasPool.get_global_ptr().load_atlas(
#     "default", "Res/atlas.txt", "Res/atlas.png")
import direct.directbase.DirectStart

import math

from panda3d.lui import *

fontPool = LUIFontPool.get_global_ptr()
luiRegion = LUIRegion.make("test", base.win)
luiTop = luiRegion.root()

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")


node = LUIObject(parent=luiTop, x=10.0, y=10.0, w=500, h=50)

texts = []

for i in xrange(10):
    texts.append(LUIText(parent=node, text="|^?,.'"))
    texts[-1].set_font_size(50)
    texts[-1].set_top(60*i)
    texts[-1].set_right(0)

node.set_pos(100, 100)
sprite = node.attach_sprite("Res/demo_textures/0.png")
sprite.set_size(500, 50)
sprite.set_relative_z_index(-0.5)
luiTop.ls()

def update(task):
    rn = random.random()

    for i, text in enumerate(texts):
        text.set_text(str(rn))
    return task.cont


base.addTask(update, "update")
# text.set_font_size(100)

# text.set_text("Hallo")

# luiTop.ls()

base.run()

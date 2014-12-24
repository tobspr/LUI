# -*- encoding: UTF-8 -*-
import sys
sys.path.insert(0, "../")
import random
from panda3d.core import *
# from panda3d.lui import *
loadPrcFileData("", "notify-level-lui info")
# loadPrcFileData("", "notify-level spam")

loadPrcFileData("", "text-pixels-per-unit 30")
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "text-minfilter linear")
loadPrcFileData("", "text-magfilter linear")
loadPrcFileData("", "depth-bits 32")
loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "gl-debug #t")
# loadPrcFileData("", "text-scale-factor 1.0")
loadPrcFileData("", "text-page-size 256 256")
# loadPrcFileData("", "framebuffer-multisample #t")
# loadPrcFileData("", "multisamples 16")
# LUIAtlasPool.get_global_ptr().load_atlas(
#     "default", "Res/atlas.txt", "Res/atlas.png")
import direct.directbase.DirectStart

import math

from panda3d.lui import *

fontPool = LUIFontPool.get_global_ptr()
luiRegion = LUIRegion.make("test", base.win)
luiTop = luiRegion.root()

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")


node2 = LUIObject(parent=luiTop, x=10.0, y=10.0, w=500, h=50)

texts = []

node2.set_pos(100, 100)
sprite2 = LUISprite(node2, "../Res/blank.png", x=0, y=100)
sprite2.set_size(500, 250)
sprite2.z_offset = 0
sprite2.set_color(1.0,0.6,0.2)
# luiTop.ls()


for i in xrange(200):
    texts.append(LUIText(node2, u"text"))
    texts[-1].set_font_size(5)
    texts[-1].set_top(2*i)
    texts[-1].set_right(0)
    texts[-1].z_offset = 500

for i in xrange(200):
    texts.append(LUIText(node2, u"text"))
    texts[-1].set_font_size(5)
    texts[-1].set_top(2*i)
    texts[-1].set_left(0)
    texts[-1].z_offset = 500

for text in texts:
    rn = random.random()
    text.set_text(unicode(rn)*5 + "...")

node = LUIObject(parent=luiTop, x=10.0, y=10.0, w=500, h=250)
node.set_pos(100, 100)
sprite = LUISprite(node, "../Res/blank.png")
sprite.set_size(500, 50)
sprite.z_offset = 0
sprite.set_color(0.2,0.6,1.0, 0.5)
# luiTop.ls()


def update(task):
    # rn = unicode(random.randint(10**10, 10**11 - 1))

    # for i, text in enumerate(texts):
        # text.set_text(unicode(random.randint(10**10, 10**11 - 1)))
    return task.cont


base.addTask(update, "update")
# text.set_font_size(100)

# text.set_text("Hallo")

# luiTop.ls()

base.run()

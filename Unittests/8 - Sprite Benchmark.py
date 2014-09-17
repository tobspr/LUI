
import sys
import time

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

from random import random

# loadPrcFileData("", "notify-level-lui spam")

loadPrcFileData("", """
sync-video #f
text-minfilter linear
text-magfilter linear
text-pixels-per-unit 40
""")


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)

parent = LUIObject(parent=region.root(), x=15, y=70, w=600, h=600)

a = time.time()

numRows = 256

print "Creating sprites .."
for x in xrange(numRows):
    for y in xrange(numRows):
        sprite = parent.attach_sprite("blank", "default")
        sprite.set_size(2, 2)
        sprite.set_top(y * 2)
        sprite.set_left(x * 2)
        sprite.set_color(random(), random(), random())

d = (time.time() - a) * 1000.0

print "Took", d, "ms to create", numRows * numRows, "sprites\n -> that's", d / float(numRows ** 2), "ms per sprite"


def test():

    print "Moving all sprites 20 times"
    start = time.time()
    for i in xrange(20):
        parent.set_top(parent.get_top() + 1)

    dur = time.time() - start
    durMs = dur * 1000.0
    durIter = durMs / 20.0
    durSprite = durIter / float(numRows ** 2)
    print durMs, "ms, that's", durIter, "per move"
    print " -> that is ", durSprite, "per sprite"


LUIText(
    parent=region.root(),
    text="Press 'p' to run a benchmark",
    font_name="default",
    font_size=20,
    x=15, y=15)

LUIText(
    parent=region.root(),
    text="Each 'pixel' is a sprite. Total Count: " + str(numRows * numRows),
    font_name="default",
    font_size=15,
    x=15, y=42)



base.accept("p", test)
base.accept("f3", region.toggle_render_wireframe)


base.run()

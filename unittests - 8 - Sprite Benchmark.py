
import sys
import time

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

# loadPrcFileData("", "notify-level-lui spam")
loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)

parent = LUIObject(parent=region.root(), x=0, y=0, w=600, h=600)

a = time.time()


print "Creating sprites .."
for x in xrange(512):
    for y in xrange(512):
        sprite = parent.attach_sprite("Res/demo_textures/0.png")
        sprite.set_size(1, 1)
        sprite.set_top(y)
        sprite.set_right(x)

d = (time.time() - a) * 1000.0

print "Took", d, "ms to create", 512 * 512, "sprites\n -> that's", d / (512.0 * 512.0), "ms per sprite"


def test():

    print "Moving all sprites 20 times"
    start = time.time()
    for i in xrange(20):
        parent.set_top(parent.get_top() + 5)

    dur = time.time() - start
    durMs = dur * 1000.0
    durIter = durMs / 20.0
    durSprite = durIter / (512.0 * 512.0)
    print durMs, "ms, that's", durIter, "per move"
    print " -> that is ", durSprite, "per sprite"


t = LUIText(parent=region.root(), text="Press 'p' to run a benchmark",
            font_name="default", x=10, y=10)
t.set_font_size(20)
t.set_relative_z_index(100)

base.accept("p", test)

base.run()

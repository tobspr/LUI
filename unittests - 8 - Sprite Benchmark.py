
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

# parent = LUIObject(parent=region.root())

for x in xrange(128):
    for y in xrange(128):
        sprite = region.root().attach_sprite("Res/demo_textures/" + str(x)+ ".png")
        sprite.set_size(1,1)
        sprite.set_top(y)
        sprite.set_right(x)


def test():

    start = time.time()
    # for i in xrange(20):
        # parent.set_top(parent.get_top() + 5)

    dur = time.time() - start
    durMs = dur * 1000.0
    durIter = durMs / 20.0
    durSprite = durIter / (512.0*512.0)
    print durMs, "ms, that's", durIter,"per iteration"
    print "that is ",durSprite,"per sprite"



base.accept("p", test)

base.run()

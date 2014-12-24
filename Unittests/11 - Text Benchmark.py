
import sys
import time
import random

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

# loadPrcFileData("", "notify-level-lui spam")
loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

import direct.directbase.DirectStart

region = LUIRegion.make("LUI", base.win)

parent = LUIObject(parent=region.root(), x=0, y=0, w=600, h=600)

a = time.time()


print "Creating Text .."

t = LUIText(parent=region.root(), text=u"Press 'p' to run a benchmark",
            font_name="default", font_size=30, x=10, y=10)


t.set_font_size(20)
# t.set_relative_z_index(100)



def test():

    iterations = 50000
    print "Setting text", iterations, "times"
    start = time.time()
    for i in xrange(iterations):
        txt = u"#" * random.randint(10,100)
        # print txt
        t.set_text(txt)

    dur = time.time() - start
    durMs = dur * 1000.0
    durIter = durMs / float(iterations)

    print durMs, "ms, that's", durIter, "ms per change"

test()
# base.accept("p", test)

base.run()

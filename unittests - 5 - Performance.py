
import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIAtlasPool, LUIRoot

from panda3d.core import loadPrcFileData
import time

loadPrcFileData("", "notify-level-lui spam")


class TestCase(LUINode):

    def __init__(self):
        LUINode.__init__(self, 100, 100)

    def test(self):
        
        print "\nAllocating a lot of children"


        start = time.time()
        iterations = 10
        for i in xrange(iterations):
            sprite = self.attach_sprite("Res/btn_left.png", i * 10, 0)
            # sprite.set_right(50)
        dur = (time.time() - start) * 1000.0
        print iterations,"Iterations in",round(dur,2),"ms, that is",round(dur/iterations,8),"ms per iteration"

        print "\nMoving a lot of children"
        for i in xrange(self.get_sprite_count()):
            self.get_sprite(i).set_left(10)

        start = time.time()
        iterations = self.get_sprite_count()
        for i in xrange(self.get_sprite_count()):
            self.get_sprite(i).set_texture("Res/btn_left.png")

        dur = (time.time() - start) * 1000.0
        print iterations,"Iterations in",round(dur,2),"ms, that is",round(dur/iterations,8),"ms per iteration"

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

ui = LUIRoot(512, 512)
test = TestCase()
ui.node().add_child(test)
test.test()

print "Deattaching .."
ui.node().remove_child(test)
del test

print "Memory should be deallocated now .."
# raw_input("test")


import sys
import time

sys.path.insert(0, "../")

from panda3d.core import loadPrcFileData, TexturePool

print "Setting level to ERROR"
loadPrcFileData("", "notify-level-lui error")

from LUI import LUIObject, LUIAtlasPool, LUIRoot


class TestCase(LUIObject):

    def __init__(self):
        LUIObject.__init__(self, 100, 100)

    def test(self):

        print "\n\nAdding children with attach_sprite"

        src1 = TexturePool.loadTexture("Res/btn_left.png")
        src2 = TexturePool.loadTexture("Res/btn_right.png")

        start = time.time()
        iterations = 11
        for i in xrange(iterations):
            sprite = self.attach_sprite(src1, i * 10, 0)
            # sprite.set_right(50)
        dur = (time.time() - start) * 1000.0
        print iterations, "Sprites created in", round(dur, 2), "ms, that is", round(dur / iterations, 8), "ms per sprite"


        self.ls()

        print "\n\nMoving children with set_left"
        start = time.time()
        iterations = self.get_sprite_count()
        for sprite in self.sprites():
            sprite.set_left(10)
        dur = (time.time() - start) * 1000.0
        print iterations, "Sprites moved in", round(dur, 2), "ms, that is", round(dur / iterations, 8), "ms per sprite"

        print "\n\nChanging sprite images with set_texture"
        start = time.time()
        iterations = self.get_sprite_count()
        for sprite in self.sprites():
            sprite.set_texture(src2)

        dur = (time.time() - start) * 1000.0
        print iterations, "Sprites changed in", round(dur, 2), "ms, that is", round(dur / iterations, 8), "ms per iteration"

        print "\n\nRemoving all childrens (child by child, with remove_sprite)"
        start = time.time()
        iterations = self.get_sprite_count()
        for sprite in self.sprites():
            self.remove_sprite(sprite)
        dur = (time.time() - start) * 1000.0
        print iterations, "Sprites removed in", round(dur, 2), "ms, that is", round(dur / iterations, 8), "ms per sprite"

        print "Sprites left: ", self.get_sprite_count()



        print "\n\nDone"

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

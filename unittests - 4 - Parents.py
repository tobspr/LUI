
import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIAtlasPool, LUIRoot

from panda3d.core import loadPrcFileData
loadPrcFileData("", "notify-level-lui spam")


def vec_equal(a, x, y):
    return a.get_x() == float(x) and a.get_y() == float(y)


class Children(LUINode):

    def __init__(self):
        LUINode.__init__(self, 200, 200)

        self.attach_sprite("Res/btn_left.png")
        self.get_sprite(0).set_right(0)


class Parent_Test(LUINode):

    """ Tests the positioning of the LUINode / LUISprite classes """

    def __init__(self):
        LUINode.__init__(self, 500, 500)

        self.do_tests()

    def do_tests(self):
        self.set_pos(20, 20)
        self.test_child = self.add_child(Children())
        self.set_pos(10, 10)

        assert(vec_equal(self.test_child.get_abs_pos(), 10, 10))
        self.test_child.set_right(0)
        self.test_child.set_bottom(0)
        assert(vec_equal(self.test_child.get_abs_pos(), 310, 310))
        assert(
            vec_equal(self.test_child.get_sprite(0).get_abs_pos(), 500, 310))

        print "Test passed."

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

ui = LUIRoot(512, 512)
ui2 = LUIRoot(756, 756)

test = Parent_Test()

print "\n\nReparenting node to root"
ui.node().add_child(test)

print "\n\nChanging image"
test.test_child.get_sprite(0).set_texture("Res/btn_right.png")


print "\n\nRemoving node"
ui.node().remove_child(test)

print "\n\nAttaching to new root"
ui2.node().add_child(test)


print "\n\nUI Root #1:"
ui.node().ls()
print "\n\nUI Root #2:"
ui2.node().ls()

print "\n\nRemoving sprite"
# test.test_child.remove_sprite(test.test_child.get_sprite(0))
test.remove_child(test.test_child)

print "\n\nRemoving node (should throw error)"
ui.node().remove_child(test)

print "\n\nRemoving node properly (should throw no error)"
ui2.node().remove_child(test)


print "\n\nTests Done."


import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIAtlasPool

from panda3d.core import loadPrcFileData
loadPrcFileData("", "notify-level-lui spam")


def vec_equal(a, x, y):
    return a.get_x() == float(x) and a.get_y() == float(y)


class Children(LUINode):

    def __init__(self):
        LUINode.__init__(self, 200, 200)


class Parent_Test(LUINode):

    """ Tests the positioning of the LUINode / LUISprite classes """

    def __init__(self):
        LUINode.__init__(self, 500, 500)

        self.do_tests()

    def do_tests(self):
        self.set_pos(20, 20)
        self.test_child = self.add_child(Children())
        self.set_pos(10, 10)

        print self.test_child.get_abs_pos()
        self.test_child.set_right(0)
        self.test_child.set_bottom(0)
        print self.test_child.get_abs_pos()


LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

test = Parent_Test()

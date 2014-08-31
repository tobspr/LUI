
import sys

sys.path.insert(0, "../")

from LUI import LUINode, LUIAtlasPool

from panda3d.core import loadPrcFileData, LVector2

import unittest
loadPrcFileData("", "notify-level-lui info")


def vec_equal(a, x, y):
    return a.get_x() == float(x) and a.get_y() == float(y)

class Positioning_Test(LUINode):

    """ Tests the positioning of the LUINode / LUISprite classes """

    def __init__(self):
        LUINode.__init__(self, 500, 500)
        self.do_tests()


    def do_tests(self):
        
        print "Running tests .."
        sprite = self.attach_sprite("Res/atlas.png", 20, 20)
        sprite.set_size(32, 32)

        # Check initial pos
        assert(vec_equal(sprite.get_abs_pos(), 20, 20))

        # Set parent pos
        self.set_pos(10, 10)
        assert(vec_equal(sprite.get_abs_pos(), 30, 30))

        # Revert parent pos
        self.set_pos(0, 0)
        sprite.set_pos(0, 0)
        assert(vec_equal(sprite.get_abs_pos(), 0, 0))

        # Align to right
        sprite.set_right(0)
        assert(vec_equal(sprite.get_abs_pos(), 500-32, 0))

        # Align to bottom
        sprite.set_bottom(0)
        assert(vec_equal(sprite.get_abs_pos(), 500-32, 500-32))

        # Resize
        self.set_size(600, 600)
        assert(vec_equal(sprite.get_abs_pos(), 600-32, 600-32))

        # Resize sprite
        sprite.set_size(64, 64)
        assert(vec_equal(sprite.get_abs_pos(), 600-64, 600-64))

        # Set to initial pos
        sprite.set_pos(0, 0)
        assert(vec_equal(sprite.get_abs_pos(), 0, 0))

        # This should throw a warning
        self.set_right(10)

        # Same for this
        self.set_bottom(10)

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

test = Positioning_Test()
from panda3d.core import *

loadPrcFileData("", """
notify-level-lui info
""")

import unittest
import LUI


class TestLUISprite(unittest.TestCase):

    def setUp(self):
        self.node = LUI.LUIObject(32, 32)
        self.sprite = self.node.attachSprite("test")
        self.sprite.set_size(5, 5)

    def test_LUISprite(self):

        # Test for uninitialized values
        pos = self.sprite.get_abs_pos()
        size = self.sprite.get_size()
        color = self.sprite.get_color()

        self.assertAlmostEqual(pos.get_x(), 0.0)
        self.assertAlmostEqual(pos.get_y(), 0.0)

        self.assertAlmostEqual(size.get_x(), 5.0)
        self.assertAlmostEqual(size.get_y(), 5.0)

        self.assertAlmostEqual(color.get_x(), 1.0)
        self.assertAlmostEqual(color.get_y(), 1.0)
        self.assertAlmostEqual(color.get_z(), 1.0)
        self.assertAlmostEqual(color.get_w(), 1.0)

        # Test position getters & Setters
        self.sprite.set_pos(10.0, 20.0)
        pos = self.sprite.get_abs_pos()
        self.assertAlmostEqual(pos.get_x(), 10.0)
        self.assertAlmostEqual(pos.get_y(), 20.0)

        self.sprite.set_left(15.0)
        self.assertAlmostEqual(self.sprite.get_abs_pos().get_x(), 15.0)

        self.sprite.set_right(0.0)
        self.assertAlmostEqual(self.sprite.get_abs_pos().get_x(), 32 - 5)

        # Test size getters & setters
        self.sprite.set_size(50, 60.0)
        scale = self.sprite.get_size()
        self.assertAlmostEqual(scale.get_x(), 50.0)
        self.assertAlmostEqual(scale.get_y(), 60.0)

        self.sprite.set_width(105.0)
        self.assertAlmostEqual(self.sprite.get_width(), 105.0)
        self.assertAlmostEqual(self.sprite.get_size().get_x(), 105.0)
        self.sprite.set_height(32.0)
        self.assertAlmostEqual(self.sprite.get_height(), 32.0)
        self.assertAlmostEqual(self.sprite.get_size().get_y(), 32.0)

        # Test color setters and getters
        self.sprite.set_color(0.2, 0.5, 1.0, 0.5)
        col = self.sprite.get_color()
        self.assertAlmostEqual(col.get_x(), 0.2)
        self.assertAlmostEqual(col.get_y(), 0.5)
        self.assertAlmostEqual(col.get_z(), 1.0)
        self.assertAlmostEqual(col.get_w(), 0.5)

        self.sprite.set_color(LColor(0.23, 0.54, 0.4, 0.7))
        col = self.sprite.get_color()
        self.assertAlmostEqual(col.get_x(), 0.23, 3)
        self.assertAlmostEqual(col.get_y(), 0.54, 3)
        self.assertAlmostEqual(col.get_z(), 0.4, 3)
        self.assertAlmostEqual(col.get_w(), 0.7, 3)

        self.node.ls()

if __name__ == '__main__':
    unittest.main()

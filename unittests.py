from panda3d.core import *

loadPrcFileData("", """
notify-level-lui spam
""")

import unittest
import LUI


class TestLUISprite(unittest.TestCase):

    def setUp(self):
        self.sprite = LUI.LUISprite()

    def test_LUISprite(self):

        # Test for uninitialized values
        pos = self.sprite.get_pos()
        size = self.sprite.get_size()
        texcStart = self.sprite.get_texcoord_start()
        texcEnd = self.sprite.get_texcoord_end()
        color = self.sprite.get_color()

        self.assertAlmostEqual(pos.get_x(), 0.0)
        self.assertAlmostEqual(pos.get_y(), 0.0)

        self.assertAlmostEqual(size.get_x(), 10.0)
        self.assertAlmostEqual(size.get_y(), 10.0)

        self.assertAlmostEqual(texcStart.get_x(), 0.0)
        self.assertAlmostEqual(texcStart.get_y(), 0.0)

        self.assertAlmostEqual(texcEnd.get_x(), 1.0)
        self.assertAlmostEqual(texcEnd.get_y(), 1.0)

        self.assertAlmostEqual(color.get_x(), 1.0)
        self.assertAlmostEqual(color.get_y(), 1.0)
        self.assertAlmostEqual(color.get_z(), 1.0)
        self.assertAlmostEqual(color.get_w(), 1.0)

        # Test position getters & Setters
        self.sprite.set_pos(10.0, 20.0)
        pos = self.sprite.get_pos()
        self.assertAlmostEqual(pos.get_x(), 10.0)
        self.assertAlmostEqual(pos.get_y(), 20.0)

        self.sprite.set_pos(LPoint2(12.0, 23.0))
        pos = self.sprite.get_pos()
        self.assertAlmostEqual(pos.get_x(), 12.0)
        self.assertAlmostEqual(pos.get_y(), 23.0)

        # Test size getters & setters
        self.sprite.set_size(50, 60.0)
        scale = self.sprite.get_size()
        self.assertAlmostEqual(scale.get_x(), 50.0)
        self.assertAlmostEqual(scale.get_y(), 60.0)

        self.sprite.set_size(LVector2(24.0, 46.0))
        scale = self.sprite.get_size()
        self.assertAlmostEqual(scale.get_x(), 24.0)
        self.assertAlmostEqual(scale.get_y(), 46.0)

        # Test color setters and getters
        self.sprite.set_color(0.2, 0.5, 1.0, 0.5)
        col = self.sprite.get_color()
        self.assertAlmostEqual(col.get_x(), 0.2)
        self.assertAlmostEqual(col.get_y(), 0.5)
        self.assertAlmostEqual(col.get_z(), 1.0)
        self.assertAlmostEqual(col.get_w(), 0.5)

        self.sprite.set_color(LColor(0.23, 0.54, 0.4, 0.7))
        col = self.sprite.get_color()
        self.assertAlmostEqual(col.get_x(), 0.23)
        self.assertAlmostEqual(col.get_y(), 0.54)
        self.assertAlmostEqual(col.get_z(), 0.4)
        self.assertAlmostEqual(col.get_w(), 0.7)

if __name__ == '__main__':
    unittest.main()

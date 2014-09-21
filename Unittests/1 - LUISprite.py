from panda3d.core import *

loadPrcFileData("", """
notify-level-lui info
""")

import unittest
from panda3d.lui import *


class TestLUISprite(unittest.TestCase):

    def setUp(self):
        self.node = LUIObject(x=0, y=0, w=32, h=32)
        self.sprite = LUISprite(self.node, "../Res/blank.png")
        self.sprite.size = (5, 5)

    def test_LUISprite(self):

        # Test for uninitialized values
        pos = self.sprite.abs_pos
        size = self.sprite.size
        color = self.sprite.get_color()

        self.assertAlmostEqual(pos.x, 0.0)
        self.assertAlmostEqual(pos.y, 0.0)

        self.assertAlmostEqual(size.x, 5.0)
        self.assertAlmostEqual(size.y, 5.0)

        self.assertAlmostEqual(color.x, 1.0)
        self.assertAlmostEqual(color.y, 1.0)
        self.assertAlmostEqual(color.z, 1.0)
        self.assertAlmostEqual(color.w, 1.0)

        # Test position getters & Setters
        self.sprite.set_pos(10.0, 20.0)
        pos = self.sprite.abs_pos
        self.assertAlmostEqual(pos.x, 10.0)
        self.assertAlmostEqual(pos.y, 20.0)

        self.sprite.left = 15.0
        self.assertAlmostEqual(self.sprite.abs_pos.x, 15.0)

        self.sprite.right = 0.0
        self.assertAlmostEqual(self.sprite.abs_pos.x, 32 - 5)

        # Test size getters & setters
        self.sprite.size = (50, 60.0)
        scale = self.sprite.size
        self.assertAlmostEqual(scale.x, 50.0)
        self.assertAlmostEqual(scale.y, 60.0)

        self.sprite.width = 105.0
        self.assertAlmostEqual(self.sprite.width, 105.0)
        self.assertAlmostEqual(self.sprite.size.x, 105.0)
        self.sprite.set_height(32.0)
        self.assertAlmostEqual(self.sprite.height, 32.0)
        self.assertAlmostEqual(self.sprite.size.y, 32.0)

        # Test color setters and getters
        self.sprite.color = (0.2, 0.5, 1.0, 0.5)
        col = self.sprite.color
        self.assertAlmostEqual(col.x, 0.2, 2)
        self.assertAlmostEqual(col.y, 0.5, 2)
        self.assertAlmostEqual(col.z, 1.0 ,2)
        self.assertAlmostEqual(col.w, 0.5, 2)

        self.sprite.color = LColor(0.23, 0.54, 0.4, 0.7)
        col = self.sprite.color
        self.assertAlmostEqual(col.x, 0.23, 2)
        self.assertAlmostEqual(col.y, 0.54, 2)
        self.assertAlmostEqual(col.z, 0.4, 2)
        self.assertAlmostEqual(col.w, 0.7, 2)


if __name__ == '__main__':
    unittest.main()

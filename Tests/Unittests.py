
from __future__ import print_function
from common import *

import unittest


class Test_FluidBox(unittest.TestCase):

    def test_box(self):
        container = LUIObject(parent=region.root)
        sprite = LUISprite(container, "blank", "skin")
        sprite.size = 100, 100

        render_frames()
        self.assertEqual(sprite.size, (100, 100))
        self.assertEqual(container.size, (100, 100))
        region.root.remove_all_children()

    def test_region(self):
        render_frames()
        self.assertEqual(region.root.size, (512, 512))

if __name__ == "__main__":
    unittest.main()

base.run()


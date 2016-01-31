
from __future__ import print_function

import sys
sys.path.insert(0, "../Builtin")

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

from panda3d.core import *
load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    notify-level-lui warning
    show-frame-rate-meter #f
    win-size 1 1
    window-title LUI Performance Test
    win-fixed-size #f
""")

import time
from functools import wraps
from panda3d.lui import LUIRegion, LUIObject, LUIInputHandler, LUISprite
from LUISkin import LUIDefaultSkin
from LUILayouts import LUIVerticalLayout
from LUIFrame import LUIFrame
from LUIFormattedLabel import LUIFormattedLabel
from LUIInputField import LUIInputField

base = ShowBase()
base.win.set_clear_color(Vec4(0.0, 0.0, 0.0, 1.0))
skin = LUIDefaultSkin()
skin.load()
region = LUIRegion.make("LUI", base.win)
handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(handler)
region.set_input_handler(handler)

class timeit(object):
    def __init__(self, num_iterations=100, internal_iterations=100):
        self._iterations = num_iterations
        self._internal_iterations = internal_iterations

    def __call__(self, func):
        def _wrap(*args, **kwargs):
            print("Timing", func.__name__, "..")
            start = time.time()
            for i in xrange(self._iterations):
                func(*args, **kwargs)
            duration = time.time() - start
            print(" + Total time: ", round(duration * 1000.0, 2), "ms, which is",
                  round(duration / self._iterations * 1000.0, 2), "ms per iteration")
            print(" + This is", round(duration / (self._iterations * self._internal_iterations) * 1000.0, 5),
                  "ms per internal iteration")
        return _wrap

@timeit(200, 100)
def test_01_create_lui_objects():
    for i in range(100):
        object = LUIObject(parent=region.root)
    region.root.remove_all_children()

@timeit(200, 100)
def test_02_create_lui_sprites():
    for i in range(100):
        object = LUISprite(region.root, "blank", "skin")
    region.root.remove_all_children()

@timeit(200, 500)
def test_03_reattach_lui_objects():
    object = LUIObject()
    object2 = LUIObject(parent=region.root)
    for i in range(500):
        object.parent = region.root
        object.parent = None
        object.parent = object2
        object.parent = None
    region.root.remove_all_children()

@timeit(200, 500)
def test_04_positioning():
    object = LUIObject(parent=region.root)
    for i in range(500):
        object.left = 3
        object.right = 8
        object.top = 3
        object.bottom = -2
        object.center_vertical = True
        object.center_horizontal = True
        object.centered = False, False
        object.top += 3
    region.root.remove_all_children()

@timeit(40, 10)
def test_05_vertical_layouts():
    layout = LUIVerticalLayout(parent=region.root)
    for i in range(10):
        for k in range(10):
            obj = LUIObject()
            sprite = LUISprite(obj, "blank", "skin")
            layout.add(obj)
        layout.reset()
    region.root.remove_all_children()

# Execute all tests
for f in sorted(i for i in list(locals()) if i.startswith("test_")):
    locals()[f]()

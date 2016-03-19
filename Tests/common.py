
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
    win-size 512 512
    window-title LUI Performance Test
    win-fixed-size #f
""")

import time
from functools import wraps
from LUIRegion import LUIRegion
from LUIObject import LUIObject
from LUIInputHandler import LUIInputHandler
from LUISprite import LUISprite
from LUISkin import LUIDefaultSkin
from panda3d.lui import LUIVerticalLayout
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

def render_frames():
    for i in range(3):
        base.graphicsEngine.renderFrame()

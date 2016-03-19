"""

This file shows the smallest working LUI example, on which you can base your
LUI projects.

"""

# Add lui modules to the path. This will not be required when LUI is included
# in panda.
import sys
sys.path.insert(0, "../Builtin")

# Load some builtin LUI classes. When lui is included in panda, this will be
# from direct.lui.LUIButton import LUIButton
from LUIButton import LUIButton
from LUISkin import LUIDefaultSkin
from LUIRegion import LUIRegion
from LUIInputHandler import LUIInputHandler

# Setup panda, nothing special here
from panda3d.core import load_prc_file_data
load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    show-frame-rate-meter #t
    win-size 700 600
    window-title LUI Minimal Example
""")

from direct.showbase.ShowBase import ShowBase

class Application(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Construct a new LUIRegion
        region = LUIRegion.make("LUI", base.win)

        # Construct a new InputHandler to catch and process events
        handler = LUIInputHandler()
        base.mouseWatcher.attach_new_node(handler)
        region.set_input_handler(handler)

        # Load the default LUI skin
        skin = LUIDefaultSkin()
        skin.load()

        # LUI is initialized now, so we can start adding elements, for example:
        button = LUIButton(parent=region.root, text="Hello world!", top=30, left=30)

Application().run()

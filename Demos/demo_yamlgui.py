"""
This example shows how to load an UI from an .yaml file
the system supports all lui types, keyword args, event binding, and custom python code inside the yaml file.

"""

# Add lui modules to the path. This will not be required when LUI is included
# in panda.
import sys,os,gc
sys.path.insert(0, "../Builtin")

from panda3d.core import*
from LUIEverything import*  # import every LUIElement
from direct.showbase.ShowBase import ShowBase
from yamlgui import yamlgui


# the panda3d setup just as in MinimalExample
load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    show-frame-rate-meter #t
    win-size 700 600
    window-title YAMLGUI Example
""")

base=ShowBase()
base.region = LUIRegion.make("LUI", base.win)
base.handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(base.handler)
base.region.set_input_handler(base.handler)
base.skin = LUIDefaultSkin()
base.skin.load()



gui = yamlgui(base.region.root)
guipath="menus/menu1.yaml"
if len(sys.argv) > 1:
	print sys.argv
	guipath=sys.argv[1]
else:
	print "loading default sample, menus/structure_test.yaml"
	print "to load a different sample file, call 'python B_yamlgui path/to/gui.yaml'"
if os.path.exists(guipath):
	# you can call loadGui at any time. If there is already a gui loaded, the old ui will be replaced
    gui.loadGui(guipath)
else:
	print guipath +" not found."
    
# example to remove the interface again
# gui.deleteGui()
base.run()
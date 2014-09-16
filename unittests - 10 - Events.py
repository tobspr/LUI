
import sys
import time

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "notify-level-lui spam")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "Res/atlas.txt", "Res/atlas.png")

import direct.directbase.DirectStart

print "\nCreating lui region .."
region = LUIRegion.make("LUI", base.win)

print "\nCreating input handler .."
handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(handler)
region.set_input_handler(handler)

class Testing:

    def __init__(self):

        parent = region.root()
        parent.set_relative_z_index(100)

        print "\nCreating sprite 1 .."
        sprite1 = parent.attach_sprite("blank", "default", x=100, y=100, w=100, h=100)
        print "\nCreating sprite 2 .."
        sprite2 = parent.attach_sprite("blank", "default", x=150, y=120, w=100, h=100)
        print "\nCreating sprite 3 .."
        sprite3 = parent.attach_sprite("blank", "default", x=125, y=150, w=100, h=100)

        print "\nSetting colors .."
        sprite1.set_color(0.2, 0.6, 1.0, 0.5)
        sprite2.set_color(0.4, 0.6, 1.0, 0.5)
        sprite3.set_color(0.6, 0.6, 1.0, 0.5)

        print "\nSetting z-indexes .."
        sprite1.set_relative_z_index(1)
        sprite2.set_relative_z_index(4)
        sprite3.set_relative_z_index(3)

        print "\nListing .."
        parent.ls()

        print "\nRemoving sprite"
        parent.remove_child(sprite1)


def create():
    Testing()

create()
print "\nDeleting instances .."

region.root().remove_all_children()
# 
run()

print "\nNow everything should be destructed .."
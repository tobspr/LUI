
import sys
import time

sys.path.insert(0, "../")

from panda3d.core import *
from panda3d.lui import *

loadPrcFileData("", "sync-video #f")
loadPrcFileData("", "show-frame-rate-meter #t")
# loadPrcFileData("", "notify-level-lui spam")

LUIAtlasPool.get_global_ptr().load_atlas(
    "default", "../Res/atlas.txt", "../Res/atlas.png")

import direct.directbase.DirectStart

print "\nCreating lui region .."
region = LUIRegion.make("LUI", base.win)

print "\nCreating input handler .."
handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(handler)
region.set_input_handler(handler)


class CounterFrame(LUIObject):

    def __init__(self):
        LUIObject.__init__(self, x=0,y=0,w=100, h=100)

        self.bg = self.attach_sprite("blank", "default")
        self.bg.set_color(0.2,0.6,1.0)
        self.bg.set_size(100, 100)

        self.header = LUIText(
            parent=self, 
            text="Click me!",
            font_name="default",
            font_size=16,
            x=10, y=15)

        self.txt = LUIText(
            parent=self, 
            text="1",
            font_name="default",
            font_size=30,
            x=10, y=35)

        self.count = 1
        self.bind("click", self.inc_count)
        self.bind("mouseover", self.mouseover)
        self.bind("mouseout", self.mouseout)

    def mouseover(self, event):
        self.bg.set_blue(0.6)

    def mouseout(self, event):
        self.bg.set_blue(1.0)


    def inc_count(self, event):
        self.count += 1
        print "Set text:",self.count
        self.txt.set_text(str(self.count))


class Testing:

    def __init__(self):

        parent = region.root()
        parent.set_relative_z_index(100)

        print "\nCreating sprite 1 .."
        sprite1 = parent.attach_sprite(
            "blank", "default", x=100, y=100, w=100, h=100)
        print "\nCreating sprite 2 .."
        sprite2 = parent.attach_sprite(
            "blank", "default", x=150, y=120, w=100, h=100)
        print "\nCreating sprite 3 .."
        sprite3 = parent.attach_sprite(
            "blank", "default", x=125, y=150, w=100, h=100)

        print "\nSetting colors .."
        sprite1.set_color(0.2, 0.6, 1.0, 1.0)
        sprite2.set_color(0.4, 0.6, 1.0, 1.0)
        sprite3.set_color(0.6, 0.6, 1.0, 1.0)

        print "\nSetting z-indexes .."
        sprite1.set_relative_z_index(1)
        sprite2.set_relative_z_index(4)
        sprite3.set_relative_z_index(3)

        print "\nBinding to events .."
        for sprite in [sprite1, sprite2, sprite3]:
            sprite.bind("mouseover", self.handle_event)
            sprite.bind("mouseout", self.handle_event)


        p = CounterFrame()
        p.set_pos(500, 100)
        parent.add_child(p)
        # print "\nThrowing event .."
        # sprite1.trigger_event("mouseover", "My Message", LPoint2(123,456))

        # print "\nUnbinding event .."
        # sprite1.unbind("mouseover")

        # print "\nListing .."
        # parent.ls()

        # print "\nRemoving sprite"
        # parent.remove_child(sprite1)

    def handle_event(self, event):
        # print "Event:"
        # print "\tSender:", event.get_sender()
        # print "\tEvent-Name:", event.get_name()
        # print "\tCoordinates:", event.get_coordinates()
        # print "\tMessage:", event.get_message()

        if event.get_name() == "mouseover":
            event.get_sender().set_blue(0.5)
        elif event.get_name() == "mouseout":
            event.get_sender().set_blue(1.0)



def create():
    Testing()

create()
print "\nDeleting instances .."

# region.root().remove_all_children()
#
run()

print "\nNow everything should be destructed .."

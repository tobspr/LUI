"""
This example shows how to load an UI from an .yaml file
"""

# Add lui modules to the path. This will not be required when LUI is included
# in panda.


import sys,os
sys.path.insert(0, "../")

from panda3d.core import*
from Builtin.LUIEverything import*  # import every LUIElement
from direct.showbase.ShowBase import ShowBase
from Builtin.LUIYamlLoader import LUIYamlLoader, LUIYamlDescription


# the panda3d setup just as in MinimalExample
load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    show-frame-rate-meter #t
    win-size 700 600
    window-title LUIYamlLoader Example
""")

base=ShowBase()
base.region = LUIRegion.make("LUI", base.win)
base.handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(base.handler)
base.region.set_input_handler(base.handler)
base.skin = LUIDefaultSkin()
base.skin.load()



gui = LUIYamlLoader(base.region.root)
guipath="menus/menu1.yaml"




class Menu1(LUIYamlDescription):
    filename = "menus/menu1.yaml"

    # automatically called when loading gui
    def handle_creation(self):
        # this is one of 2 ways to bind events
        # alternatively, events can be specified inside yaml
        # note that quit_button is the name set by menu1.yaml
        self.gui.quit_button.bind("click",self.handle_quit)

    def handle_menu2(self,event):
        self.gui.load_gui(Menu2)

    def handle_menu3(self,event):
        self.gui.load_gui(Menu3)

    def handle_quit(self,event):
        taskMgr.stop()



class Menu2(LUIYamlDescription):
    filename = "menus/menu2.yaml"

    def handle_backToMain(self,event):
        self.gui.load_gui(Menu1)


class Menu3(LUIYamlDescription):
    filename = "menus/menu3.yaml"

    def handle_creation(self):
        # this is a basic instancing example
        # the tree template "horizontal" is going into the graph x times
        self.gui.instance_element("horizontal", gui.vertical1, [1])
        self.gui.instance_element("horizontal", gui.vertical1, [2])
        self.gui.instance_element("horizontal", gui.vertical1, [3])

        # then, normal acces using the unique name is possible, e.g.
        self.gui.horizontal1            # "horizontal{0}".format([1]) 
        self.gui.mybutton2_2            # "mybutton{0}_2".format([2])


    def toMain(self,event):
        self.gui.load_gui(Menu1)

    def del_row(self,event):
        # to delete a instanced branch, given name and formatlist as in instance_element():
        gui.delete_instanced_element("horizontal", [2])



# to remove the interface again
# gui.delete_gui()


gui.load_gui(Menu1)
base.run()




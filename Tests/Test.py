
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
    notify-level-lui info
    show-frame-rate-meter #t
    win-size 780 630
    window-title LUI Demo
    win-fixed-size #f
""")

from LUIRegion import LUIRegion
from LUIObject import LUIObject
from LUIInputHandler import LUIInputHandler
from LUISprite import LUISprite
from LUIVerticalLayout import LUIVerticalLayout
from LUISkin import LUIDefaultSkin
from LUIFrame import LUIFrame
from LUIFormattedLabel import LUIFormattedLabel
from LUIInputField import LUIInputField
from LUIButton import LUIButton
from LUILabel import LUILabel
from LUICheckbox import LUICheckbox
from LUIRadiobox import LUIRadiobox
from LUIRadioboxGroup import LUIRadioboxGroup

s = ShowBase()
base.win.set_clear_color(Vec4(0.05, 0.05, 0.05, 1.0))

skin = LUIDefaultSkin()
skin.load()

region = LUIRegion.make("LUI", base.win)
handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(handler)
region.set_input_handler(handler)

# bg = LUISprite(region.root, "blank", "skin")
# bg.pos = 200, 200
# bg.size = 200, 300

container = LUIFrame(
    parent = region.root, pos = (200, 200), height=300,
    style = LUIFrame.FS_sunken)


# label_tl = LUILabel(parent=container, text="Top Left", top_left=(0,0))
# label_tr = LUILabel(parent=container, text="Top Right", top_right=(0,0))
# label_bl = LUILabel(parent=container, text="Bottom Left", bottom_left=(0,0))
# label_br = LUILabel(parent=container, text="Bottom Right", bottom_right=(0,0))

# button = LUIButton(parent=container, top_left=(0, 0), text="Well this one .. is a long button! (A really long one!) ............ really long!")
# button.bind("click", lambda event: button.set_text("Hello!"))
container.size = 300, 300
# group = LUIRadioboxGroup()
# box = LUIRadiobox(parent=container, group=group, top=50)
# box2 = LUICheckbox(parent=container, top=100)

layout = LUIVerticalLayout(parent=container)
# layout.height = 280
# layout.width = 300

LUILabel(parent=layout.cell(),      text="Hello")
LUILabel(parent=layout.cell(),      text="World")
LUILabel(parent=layout.cell(100),   text="100px row")
LUILabel(parent=layout.cell(),      text="Next")
LUIButton(parent=layout.cell(),     text="SomeButton")
LUILabel(parent=layout.cell('*'),   text="Fill column")
LUILabel(parent=layout.cell(),      text="Last column")

for i in range(5):
    base.graphicsEngine.render_frame()

region.root.ls()

s.run()

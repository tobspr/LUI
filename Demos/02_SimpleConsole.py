# encoding: utf-8
import sys
sys.path.insert(0, "../Builtin")
sys.path.insert(0, "../")

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

from panda3d.core import *
load_prc_file_data("", """
    notify-level-lui info
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    show-frame-rate-meter #t
    win-size 780 630
    window-title LUI Demo
    win-fixed-size #f
""")

# Imports

import codecs

from LUISkin import LUIDefaultSkin
from LUIFrame import LUIFrame
from LUILabel import LUILabel
from LUIInputField import LUIInputField
from LUIFormattedLabel import LUIFormattedLabel
from LUIScrollableRegion import LUIScrollableRegion
from LUIObject import LUIObject
from LUIRegion import LUIRegion
from LUIInputHandler import LUIInputHandler
from LUIVerticalLayout import LUIVerticalLayout

from Skins.Metro.LUIMetroSkin import LUIMetroSkin

s = ShowBase()

# Load a LUI Skin
if False:
    skin = LUIMetroSkin()
    base.win.set_clear_color(Vec4(1))
else:
    skin = LUIDefaultSkin()
    base.win.set_clear_color(Vec4(0.1, 0.0, 0.0, 1))

skin.load()

# Initialize LUI
region = LUIRegion.make("LUI", base.win)
handler = LUIInputHandler()
base.mouseWatcher.attach_new_node(handler)
region.set_input_handler(handler)

# Title
title_label = LUILabel(parent=region.root, text="LUI Console Example", font_size=40,
                       font="header", pos=(25, 17))

# Container
container = LUIFrame(parent = region.root, width=700, height=500,
    style=LUIFrame.FS_sunken, margin=30, top=50)

text_container = LUIScrollableRegion(parent=container, width=675, height=440,
    padding=0)

base.win.set_clear_color(Vec4(0.1, 0.1, 0.1, 1.0))
layout = LUIVerticalLayout(parent=text_container.content_node)

def send_command(event):
    """ Called when the user presses enter in the input field, submits the
    command and prints something on the console """
    label = LUIFormattedLabel()
    color = (0.9, 0.9, 0.9, 1.0)
    if event.message.startswith(u"/"):
        color = (0.35, 0.65, 0.24, 1.0)
    label.add(text=">>>  ", color=(0.35, 0.65, 0.24, 1.0))
    label.add(text=event.message, color=color)
    layout.add(label)

    result = LUIFormattedLabel()
    result.add("Your command in rot13: " + codecs.encode(event.message, "rot13"), color=(0.4, 0.4, 0.4, 1.0))
    layout.add(result)
    input_field.clear()

    text_container.scroll_to_bottom()

# Create the input box
input_field = LUIInputField(parent=container, bottom=0, left=0, width="100%")
input_field.bind("enter", send_command)
input_field.request_focus()

# Add some initial commands
for demo_command in ["Hello world!", "This is a simple console", "You can type commands like this:", "/test"]:
    input_field.trigger_event("enter", demo_command)

s.run()



from DemoFramework import DemoFramework
from LUIRadiobox import LUIRadiobox
from LUIRadioboxGroup import LUIRadioboxGroup
from LUIVerticalLayout import LUIVerticalLayout

import random

f = DemoFramework()
f.prepare_demo("LUIRadiobox")

# Constructor
f.add_constructor_parameter("group", "None")
f.add_constructor_parameter("value", "None")
f.add_constructor_parameter("label", "'Radiobox'")

# Functions
f.add_public_function("get_value", [], "object")
f.add_public_function("get_label", [], "LUILabel")
f.add_public_function("set_active", [], "void")

f.add_property("value", "object")
f.add_property("label", "LUILabel")

# Events
f.add_event("changed")
f.construct_sourcecode("LUIRadiobox")

# Create a group to connect the boxes
group = LUIRadioboxGroup()

# Create a layout for the boxes
grid = LUIVerticalLayout(parent=f.get_widget_node(), spacing=5)

# Create the boxes
boxes = []
for i in range(1, 4):
    boxes.append(LUIRadiobox(group=group, value=i, label="Radiobox {0}".format(i), active=i==2))
    grid.add(boxes[-1])

f.set_actions({
        "Select Box 1": lambda: boxes[0].set_active(),
        "Select Box 2": lambda: boxes[1].set_active(),
        "Select Box 3": lambda: boxes[2].set_active(),
        "Set Random Text": lambda: boxes[0].label.set_text("Text: " + str(random.randint(100, 10000))),
    })

run()

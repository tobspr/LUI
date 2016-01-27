

from DemoFramework import DemoFramework
from LUIRadiobox import LUIRadiobox
from LUIRadioboxGroup import LUIRadioboxGroup
from LUILayouts import LUIVerticalLayout

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

# Events
f.add_event("changed")
f.construct_sourcecode("LUIRadiobox")

# Create a group to connect the boxes
group = LUIRadioboxGroup()

# Create a layout for the boxes
grid = LUIVerticalLayout(parent=f.get_widget_node(), width=250, spacing=5)   

# Create 3 boxes
box1 = LUIRadiobox(group=group, value=1, label="Radiobox 1")
box2 = LUIRadiobox(group=group, value=2, label="Radiobox 2", active=True)
box3 = LUIRadiobox(group=group, value=3, label="Radiobox 3")

# Add 3 boxes
grid.add(box1)
grid.add(box2)
grid.add(box3)

f.set_actions({
        "Select Box 1": lambda: box1.set_active(),
        "Select Box 2": lambda: box2.set_active(),
        "Set Random Text": lambda: box1.get_label().set_text(unicode(random.randint(100, 10000))),
    })

run()

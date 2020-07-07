

from DemoFramework import DemoFramework
from LUICheckbox import LUICheckbox

import random

f = DemoFramework()
f.prepare_demo("LUICheckbox")

# Constructor
f.add_constructor_parameter("checked", "False")
f.add_constructor_parameter("label", "'Checkbox'")

# Functions
f.add_public_function("get_checked", [], "bool")
f.add_public_function("toggle_checked", [], "bool")
f.add_public_function("set_checked", [("checked", "bool")])
f.add_public_function("get_label", [], "UILabel")

f.add_property("checked", "bool")
f.add_property("label", "LUILabel")

# Events
f.add_event("changed")
f.construct_sourcecode("LUICheckbox")

# Create the checkbox
checkbox = LUICheckbox(parent=f.get_widget_node())

f.set_actions({
        "Set Checked": lambda: checkbox.set_checked(True),
        "Set Unchecked": lambda: checkbox.set_checked(False),
        "Toggle Checked": lambda: checkbox.toggle_checked(),
        "Set Random Text": lambda: checkbox.get_label().set_text("Text: " + str(random.randint(100, 10000))),
    })

run()

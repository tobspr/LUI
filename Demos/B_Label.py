

from DemoFramework import DemoFramework
from LUILabel import LUILabel

import random

f = DemoFramework()
f.prepare_demo("LUILabel")

# Constructor

f.add_constructor_parameter("text", "Label")
f.add_constructor_parameter("shadow", "True")
f.add_constructor_parameter("font_size", "14")
f.add_constructor_parameter("font", "'label'")

# Functions
f.add_public_function("get_text", [], "string")
f.add_public_function("set_text", [("text", "string")])

f.add_property("text", "string")
f.add_property("text_handle", "LUIText")

# Events
f.construct_sourcecode("LUILabel")

# Create a new label
label = LUILabel(parent=f.get_widget_node(), text="This is a fancy label")

f.set_actions({
        "Set Random Text": lambda: label.set_text(str(random.randint(100, 10000))),
        "Set Random Color": lambda: label.set_color(random.random(), random.random(), random.random(), 1)
    })

run()

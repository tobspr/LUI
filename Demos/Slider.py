

from DemoFramework import DemoFramework
from LUISlider import LUISlider

import random

f = DemoFramework()
f.prepare_demo("LUISlider")

# Constructor
f.add_constructor_parameter("filled", "False")
f.add_constructor_parameter("min_value", "0.0")
f.add_constructor_parameter("max_value", "0.0")
f.add_constructor_parameter("value", "None")

# Functions
f.add_public_function("get_value", [], "float")
f.add_public_function("set_value", [("value", "float")])

f.add_property("value", "float")

# Events
f.add_event("changed")
f.construct_sourcecode("LUISlider")

# Create the checkbox
slider = LUISlider(parent=f.get_widget_node(), width=200.0)
slider_nofill = LUISlider(parent=f.get_widget_node(), width=200.0, filled=False, top=30)



f.set_actions({
        "Set to 30%": lambda: slider.set_value(0.3),
    })

run()

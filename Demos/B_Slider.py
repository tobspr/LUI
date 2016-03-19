

from DemoFramework import DemoFramework
from LUISlider import LUISlider
from LUILabel import LUILabel
from LUIVerticalLayout import LUIVerticalLayout

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
layout = LUIVerticalLayout(parent=f.get_widget_node(), spacing=10)

LUILabel(parent=layout.cell(), text="This is a filled slider:", color=(1, 1, 1, 0.4))
slider = LUISlider(parent=layout.cell(), width=200.0)

LUILabel(parent=layout.cell(), text="This is a regular slider:", color=(1, 1, 1, 0.4))
slider_nofill = LUISlider(parent=layout.cell(), width=200.0, filled=False)

f.set_actions({
        "Set to 30%": lambda: slider.set_value(0.3),
    })

run()

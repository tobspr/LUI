

from DemoFramework import DemoFramework
from LUIProgressbar import LUIProgressbar
from LUISlider import LUISlider
from LUILabel import LUILabel
from LUIVerticalLayout import LUIVerticalLayout

import random

f = DemoFramework()
f.prepare_demo("LUIProgressbar")

# Constructor
f.add_constructor_parameter("show_label", "False")

# Functions
f.add_public_function("get_value", [], "float")
f.add_public_function("set_value", [("value", "float")])

f.add_property("value", "float")

# Events
f.construct_sourcecode("LUIProgressbar")

# Create the checkbox
layout = LUIVerticalLayout(parent=f.get_widget_node(), spacing=10)

LUILabel(parent=layout.cell(), text="This is a progressbar:", color=(1, 1, 1, 0.4))
bar = LUIProgressbar(parent=layout.cell(), width=200.0)

LUILabel(parent=layout.cell(), text="You can control it with this slider:", color=(1, 1, 1, 0.4))
slider = LUISlider(parent=layout.cell(), width=200.0, filled=True)
slider.bind("changed", lambda event: bar.set_value(slider.value * 100.0))

f.set_actions({
        "Set to 30%": lambda: bar.set_value(30),
    })

run()

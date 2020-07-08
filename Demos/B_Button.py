
from DemoFramework import DemoFramework
from LUIButton import LUIButton
from LUIHorizontalLayout import LUIHorizontalLayout

import random

f = DemoFramework()
f.prepare_demo("LUIButton")

# Constructor
f.add_constructor_parameter("text", "u'Button'")
f.add_constructor_parameter("template", "'ButtonDefault'")

# Functions
f.add_public_function("set_text", [("text", "string")])
f.add_public_function("get_text", [], "string")
f.add_property("text", "string")

# Construct source code
f.construct_sourcecode("LUIButton")

# Create 2 new buttons, and store them in a vertical layout
layout = LUIHorizontalLayout(parent=f.get_widget_node(), spacing=10)

button1 = LUIButton(text="Do not click me")
button2 = LUIButton(text="Instead click me", template="ButtonGreen")

layout.add(button1)
layout.add(button2)

f.set_actions({
        "Set Random Text": lambda: button1.set_text("Text: " + str(random.randint(100, 10000000))),
    })

run()

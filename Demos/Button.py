

from DemoFramework import DemoFramework
from LUIButton import LUIButton

import random

f = DemoFramework()
f.prepare_demo("LUIButton")

# Constructor

f.add_constructor_parameter("text", "u'Button'")
f.add_constructor_parameter("template", "'ButtonDefault'")


# Functions
f.add_public_function("set_text", [("text", "string")])
f.add_public_function("get_text", [], "string")

# Events
f.construct_sourcecode("LUIButton")

# Create 2 new buttons
button1 = LUIButton(parent=f.get_widget_node(), text="Do not click me")
button2 = LUIButton(parent=f.get_widget_node(), text="Instead click me", template="ButtonMagic", left=button1.width + 10)



# f.set_actions({
#         "Set Random Text": lambda: label.set_text(unicode(random.randint(100, 10000))),
#     })

run()

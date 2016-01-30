
from DemoFramework import DemoFramework
from LUIInputField import LUIInputField

import random

f = DemoFramework()
f.prepare_demo("LUIInputField")

# Constructor
f.add_constructor_parameter("value", "u''")
f.add_constructor_parameter("placeholder", "u'Enter some text ..'")
f.add_property("value", "string")
f.add_event("changed")

# Construct source code
f.construct_sourcecode("LUIInputField")

# Create 2 new buttons, and store them in a vertical layout
field = LUIInputField(parent=f.get_widget_node())

f.set_actions({
        "Set Random Text": lambda: field.set_value(u"Text: " + unicode(random.randint(100, 10000000))),
        "Clear": lambda: field.clear(),
    })

run()

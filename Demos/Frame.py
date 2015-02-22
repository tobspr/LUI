

from DemoFramework import DemoFramework
from LUIFrame import LUIFrame

import random

f = DemoFramework()
f.prepare_demo("LUIFrame")

# Constructor
f.add_constructor_parameter("width", "200")
f.add_constructor_parameter("height", "200")
f.add_constructor_parameter("innerPadding", "5")
f.add_constructor_parameter("scrollable", "False")
f.add_constructor_parameter("style", "UIFrame.Raised")

# Functions

# Events
# f.add_event("changed")
f.construct_sourcecode("LUIFrame")

frame = LUIFrame(width=300, height=100, parent=f.get_widget_node())

f.set_actions({
        "Resize to 100x100": lambda: frame.set_size(100, 100),
        "Resize to 150x150": lambda: frame.set_size(150, 150),
        "Fit to children": lambda: frame.fit_to_children(),
        "Resize to Random Size": lambda: frame.set_size(random.randint(10, 150), random.randint(10, 150)),
    })

run()
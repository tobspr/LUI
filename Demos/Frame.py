

from DemoFramework import DemoFramework
from LUIFrame import LUIFrame
from LUILabel import LUILabel
from LUILayouts import LUIVerticalLayout
from panda3d.lui import LUIObject

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
f.construct_sourcecode("LUIFrame")

# Construct a new frame
frame = LUIFrame(width=300, height=100, parent=f.get_widget_node())

layout = LUIVerticalLayout(parent=frame, width=160, spacing=10)
layout.add(LUILabel(text=u"This is some frame", color=(0.2, 0.6, 1.0, 1.0)))
layout.add(LUILabel(text=u"Here is another line of text"))
layout.add(LUILabel(text=u"And even more text."))

f.set_actions({
        "Resize to 200x100": lambda: frame.set_size(200, 100),
        "Resize to 200x120": lambda: frame.set_size(200, 120),
        "Fit to children": lambda: frame.fit_to_children(),
    })

run()

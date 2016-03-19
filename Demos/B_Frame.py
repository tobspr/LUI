

from DemoFramework import DemoFramework
from LUIVerticalLayout import LUIVerticalLayout
from LUIFrame import LUIFrame
from LUILabel import LUILabel
from LUIButton import LUIButton
from LUIObject import LUIObject

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
frame = LUIFrame(parent=f.get_widget_node())

layout = LUIVerticalLayout(parent=frame, spacing=5)
layout.add(LUILabel(text="This is some frame ..", color=(0.2, 0.6, 1.0, 1.0), font_size=20))
layout.add(LUILabel(text="It can contain arbitrary elements."))
layout.add(LUILabel(text="For example this button:"))
layout.add(LUIButton(text="Fancy button"))

# frame.fit_to_children()

f.set_actions({
        "Resize to 300x160": lambda: frame.set_size(300, 160),
        "Fit to children": lambda: frame.clear_size(),
    })

run()

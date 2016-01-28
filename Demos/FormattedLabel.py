

from DemoFramework import DemoFramework
from LUIFormattedLabel import LUIFormattedLabel

import random

f = DemoFramework()
f.prepare_demo("LUIFormattedLabel")

# Functions
f.add_public_function("clear", [], "void")
f.add_public_function("br", [], "void")
f.add_public_function("add_text", [("*args", "List"), ("**kwargs", "Dict")])

# Events
f.construct_sourcecode("LUIFormattedLabel")

# Create a new label
label = LUIFormattedLabel(parent=f.get_widget_node())

# Add parts to the label
label.add_text(text="Hello ", color=(0.2,0.6,1.0))
label.add_text(text="World", color=(1.0,0.6,0.2))
label.add_text(text="! ")
label.add_text(text="This ", font_size=20, margin_top=-6, color=(0.4,0.2,1.0))
label.add_text(text="is ", color=(1.0,0.2,1.0))
label.add_text(text="a formatted ", font_size=10, color=(0.6,0.3,0.6))
label.add_text(text="Label", font_size=25, margin_top=-11, color=(0.2,1.0,0.6))

# Go to next line
label.br()
label.br()

# Add some more parts
label.add_text(text="This is the same label ..", color=(0.3,0.7,0.32))

# Go to next line
label.br()
label.br()

# Add some more parts
label.add_text(text="... but another line forced with ", color=(0.6,0.3,0.8))
label.add_text(text="br() ", color=(1.0,0.6,0.2))

def make_random_color():
    return (random.random(), random.random(), random.random())

def newline():
    label.br()
    label.add_text(text="New Line!", color=make_random_color())

f.set_actions({
        "Add random text": lambda: label.add_text(text="Text ", color=make_random_color()),
        "Go to next line": newline
    })

run()

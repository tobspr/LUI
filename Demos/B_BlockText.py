

from DemoFramework import DemoFramework
from LUILabel import LUILabel
from LUIBlockText import LUIBlockText
from LUIScrollableRegion import LUIScrollableRegion

import random

f = DemoFramework()
f.prepare_demo("LUIBlockText")

# Constructor

f.add_constructor_parameter("text", "u'Label'")
f.add_constructor_parameter("shadow", "True")
f.add_constructor_parameter("font_size", "14")
f.add_constructor_parameter("font", "'label'")

# Functions
f.add_public_function("clear", [])
f.add_public_function("set_text", [("text", "string")])
f.add_public_function("set_wrap", [("wrap", "boolean")])
f.add_public_function("set_width", [("width", "integer")])

f.add_property("labels", "list")

# Events
f.construct_sourcecode("LUIBlockText")

text_container = LUIScrollableRegion(
	parent=f.get_widget_node(),
	width=340,
	height=190,
    padding=0,
)

#TODO: Support newline through charcode 10
#TODO: If space causes next line, dont print it

# Create a new label
label = LUIBlockText(parent=text_container, width=310)

# Paragraph with no line breaks
label.add(
	text='''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed malesuada sit amet erat non gravida.  Pellentesque sit amet cursus risus Sed egestas, nulla in tempor cursus, ante felis cursus magna, nec vehicula nisi nulla eu nulla.''',
	color=(0.9,0.9,.9),
	wordwrap=True,
	padding=5,
)


# Paragraph with some linebreaks
label.add(
	text='''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed malesuada sit amet erat non gravida.
Pellentesque sit amet cursus risus Sed egestas, nulla in tempor cursus, ante felis cursus magna, nec vehicula nisi nulla eu nulla.
Nulla sed pellentesque erat.  Morbi facilisis at erat id auctor.  Phasellus euismod facilisis sem, at molestie velit condimentum sit amet.

Nulla posuere rhoncus aliquam.''',
	color=(0.9,0.9,.9),
	wordwrap=True,
	padding=5,
)

# Paragraph with no spaces or linebreaks
label.add(
	text='''Loremipsumolorsitamet,consecteturadipiscingelit.Sedmalesuadasitameteratnongravida.PellentesquesitametcursusrisusSedegestas,nullaintemporcursus,antefeliscursusmagna,necvehiculanisinullaeunulla.''',
	color=(0.9,0.9,.9),
	wordwrap=True,
	padding=5,
)

def setWidth(width):
	label.set_width(width)
	text_container.on_element_added()

def setWrap(wrap):
	label.set_wrap(wrap)
	text_container.on_element_added()


f.set_actions({
        "Set Random Text": lambda: label.set_text(str(random.randint(100, 10000))),
        "Set Random Color": lambda: label.set_color((random.random(), random.random(), random.random(), 1)),
        "Clear": lambda: label.clear(),
        "Smaller": lambda: setWidth(200),
        "Larger": lambda: setWidth(310),
        "Wrapping on": lambda: setWrap(True),
        "Wrapping off": lambda: setWrap(False),
    })

base.run()

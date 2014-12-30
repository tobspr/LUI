

from DemoFramework import DemoFramework
from UICheckbox import UICheckbox

f = DemoFramework()
f.prepare_demo("UICheckbox")


# Constructor
f.add_constructor_parameter("checked", "False")
f.add_constructor_parameter("label", "'Checkbox'")

# Functions
f.add_public_function("get_checked", [], "bool")
f.add_public_function("set_checked", [("checked", "bool")])
f.add_public_function("get_label", [], "UILabel")

# Events
f.add_event("changed")
f.construct_sourcecode("UICheckbox")

checkbox = UICheckbox()
checkbox.parent = f.get_widget_node()



f.set_actions({
        "Set Checked": lambda: checkbox.set_checked(True),
        "Set Unchecked": lambda: checkbox.set_checked(False),
    })



run()

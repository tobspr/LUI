

import sys
sys.path.insert(0, "../Builtin")

from panda3d.core import *
from panda3d.lui import LUIRegion, LUIInputHandler, LUISprite, LUIObject

from LUILabel import LUILabel
from LUIFrame import LUIFrame

load_prc_file_data("", """
    text-minfilter linear
    text-magfilter linear
    text-pixels-per-unit 32
    sync-video #f
    textures-power-2 none
    notify-level-lui info
    show-frame-rate-meter #f
    win-size 780 630
    window-title LUI Demo
    win-fixed-size #f
""")

import direct.directbase.DirectStart
from LUISkin import LUIDefaultSkin
from LUILayouts import LUIVerticalLayout
from LUICheckbox import LUICheckbox
from LUIFormattedLabel import LUIFormattedLabel
from LUISelectbox import LUISelectbox
from LUIButton import LUIButton

class DemoFramework:

    """ This is a small helper class to setup common stuff for the demos """

    def __init__(self):
        base.win.set_clear_color(Vec4(0, 0, 0, 1))
        self._skin = LUIDefaultSkin()
        self._skin.load()

        # Construct the LUIRegion
        region = LUIRegion.make("LUI", base.win)
        handler = LUIInputHandler()
        base.mouseWatcher.attach_new_node(handler)
        region.set_input_handler(handler)

        self._root = region.root
        self._constructor_params = []

    def prepare_demo(self, demo_title=u"Some Demo"):

        # Background
        self._background = LUISprite(self._root, "res/DemoBackground.png")


        # Make the background solid and recieve events
        self._background.solid = True

        # Logo
        self._logo = LUISprite(self._root, "res/LUILogo.png")
        self._logo.top = 15
        self._logo.left = 20

        # Title
        self._title_label = LUILabel(parent=self._root, text=demo_title, font_size=40,
                                     font="header", pos=(120, 27))
        self._subtitle_label = LUILabel(parent=self._root, text="Widget Demo", font_size=14,
                                        font="default", pos=(121, 65), color=(1, 1, 1, 0.5))

        # Right bar
        self._right_bar = LUIVerticalLayout(parent=self._root, width=350, spacing=20)
        self._right_bar.pos = (410, 120)

        # Constructor parameters
        # self._constructor_parameter_frame = LUIFrame(width=340, style=LUIFrame.FS_sunken)
        # self._constructor_label = LUILabel(parent=self._constructor_parameter_frame, text=u"Additional Constructor Parameters")
        # self._constructor_layout = UIVerticalLayout(parent=self._constructor_parameter_frame, spacing=10, use_dividers=True)
        # self._constructor_layout.top = 30

        # Public functions
        self._public_functions = LUIFrame(width=340, style=LUIFrame.FS_sunken)
        self.functions_label = LUILabel(parent=self._public_functions, text=U"Additional Public functions")
        self.functions_layout = LUIVerticalLayout(parent=self._public_functions,spacing=10, use_dividers=True, top=30)

        # Events
        self._events = LUIFrame(width=340, style=LUIFrame.FS_sunken)
        self._events_label = LUILabel(parent=self._events, text=U"Additional Events")
        self._events_layout = LUIVerticalLayout(parent=self._events, spacing=10, use_dividers=True, top=30)

        # Actions
        self._actions = LUIFrame(width=340, style=LUIFrame.FS_sunken, height=80)
        self._actions_label = LUILabel(parent=self._actions, text=U"Demo-Actions")
        self._actions_select = LUISelectbox(parent=self._actions, width=245, top=30)
        self._actions_btn = LUIButton(parent=self._actions, right=0, top=30, text=u"Execute", template="ButtonGreen")
        self._actions_btn.bind("click", self._exec_action)

        # Properties
        self._properties = LUIFrame(width=340, style=LUIFrame.FS_sunken)
        self._properties_label = LUILabel(parent=self._properties, text=u"Additional Properties")
        self._properties_layout = LUIVerticalLayout(parent=self._properties, spacing=10, use_dividers=True, top=30)

        self._right_bar.add(self._actions)
        self._right_bar.add(self._public_functions)
        self._right_bar.add(self._properties)
        self._right_bar.add(self._events)

        # Widget
        self._widget_container = LUIFrame(parent=self._root, width=360, height=250, style=LUIFrame.FS_sunken)
        self._widget_label = LUILabel(parent=self._widget_container, text=u"Widget Demo")
        self._widget_container.left = 26
        self._widget_container.top = 120

        # Source Code
        self._source_container = LUIFrame(parent=self._root, width=360, height=200, style=LUIFrame.FS_sunken)
        self._source_label = LUILabel(parent=self._source_container, text=u"Default Constructor")
        self._copy_code_button = LUIButton(parent=self._source_container,
                text=u"Copy to Clipboard", template="ButtonGreen",
                right=-5, bottom=-5)
        self._source_container.left = 26
        self._source_container.top = 390
        self._source_content = LUIObject(self._source_container)
        self._source_content.top = 40

        self._widget_node = LUIObject(self._widget_container, x=0, y=40)

    def _exec_action(self, event):
        selected = self._actions_select.get_selected_option()
        if selected is not None:
            selected()

    def set_actions(self, actions):
        opts = []

        for name, action in actions.items():
            opts.append((action, name))

        self._actions_select.set_options(opts)

    def add_public_function(self, name, parameters=None, return_type="void"):
        label = LUIFormattedLabel()
        label.add(text=return_type + " ", color = (102/255.0, 217/255.0, 239/255.0))
        label.add(text=name + " ", color = (166/255.0, 226/255.0, 46/255.0))

        label.add(text="( ", color=(0.9,0.9,0.9))

        if parameters is not None:
            for index, (pname, ptype) in enumerate(parameters):
                label.add(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
                label.add(text=" : ", color=(0.9,0.9,0.9))
                label.add(text=ptype, color=(102/255.0, 217/255.0, 239/255.0))

                if index < len(parameters) - 1:
                    label.add(text=",", color=(0.9,0.9,0.9))
        label.add(text=" )", color=(0.9,0.9,0.9))
        self.functions_layout.add(label)
        self.update_layouts()

    def add_constructor_parameter(self, name, default):
        self._constructor_params.append((name, default))
        self.update_layouts()

    def add_event(self, event_name):
        label = LUILabel(text=event_name)
        label.color = (1,1,1,0.5)
        self._events_layout.add(label)
        self.update_layouts()

    def add_property(self, property_name, property_type):
        label = LUIFormattedLabel()
        label.add(text=property_name, color=(255/255.0, 151/255.0, 31/255.0) )
        label.add(" : ", color=(0.9,0.9,0.9) )
        label.add(text=property_type + " ", color=(102/255.0, 217/255.0, 239/255.0) )
        self._properties_layout.add(label)
        self.update_layouts()

    def update_layouts(self):
        self._public_functions.fit_height_to_children()
        # self._constructor_parameter_frame.fit_height_to_children()
        self._events.fit_height_to_children()
        self._properties.fit_height_to_children()
        self._right_bar.update()

    def construct_sourcecode(self, classname):
        self._source_content.remove_all_children()
        label = LUIFormattedLabel(parent=self._source_content)
        label.add(text="element ", color=(0.9,0.9,0.9))
        label.add(text="= ", color=(249/255.0, 38/255.0, 114/255.0))
        label.add(text=classname, color=(166/255.0, 226/255.0, 46/255.0))
        label.add(text="(", color=(0.9,0.9,0.9))

        for index, (pname, pvalue) in enumerate(self._constructor_params):
            label.newline()
            label.add(text=" " * 15)
            label.add(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
            label.add(text=" = ")
            label.add(text=pvalue, color=(153/255.0, 129/255.0, 255/255.0))

            if index < len(self._constructor_params) - 1:
                label.add(text=",")

        label.add(text=")")

        copy_text = "element = " + classname + "("

        for index, (pname, pvalue) in enumerate(self._constructor_params):
            copy_text += pname + "=" + pvalue

            if index < len(self._constructor_params) - 1:
                copy_text += ", "
        copy_text += ")"

        def copy_code(event):
            # Copies the source code to clipboard
            from Tkinter import Tk
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(copy_text)
            r.destroy()

        self._copy_code_button.bind("click", copy_code)

        self._source_content.fit_height_to_children()
        self._source_container.fit_height_to_children()
        self._source_container.height += 40


    def get_widget_node(self):
        return self._widget_node

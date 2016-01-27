

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
        self.skin = LUIDefaultSkin()
        self.skin.load()

        # Construct the LUIRegion
        region = LUIRegion.make("LUI", base.win)
        handler = LUIInputHandler()
        base.mouseWatcher.attach_new_node(handler)
        region.set_input_handler(handler)

        self.root = region.root
        self.constructorParams = []

    def prepare_demo(self, demo_title=u"Some Demo"):

        # Background
        self.background = LUISprite(self.root, "res/DemoBackground.png")


        # Make the background solid and recieve events
        self.background.bind("click", lambda event: self.background.request_focus())
        self.background.solid = True

        # Logo
        self.logo = LUISprite(self.root, "res/LUILogo.png")
        self.logo.top = 15
        self.logo.left = 20

        # Title
        self.titleLabel = LUILabel(parent=self.root, text=demo_title, font_size=40, font="header")
        self.titleLabel.pos = (120, 20)
        self.subtitleLabel = LUILabel(parent=self.root, text="Widget Demo", font_size=14, font="default")
        self.subtitleLabel.pos = (121, 65)
        self.subtitleLabel.color = (1,1,1,0.5)

        # Right bar
        self.rightBar = LUIVerticalLayout(parent=self.root, width=350, spacing=20)
        self.rightBar.pos = (410, 120)

        # Constructor parameters
        # self.constructorParameters = LUIFrame(width=340, style=LUIFrame.Sunken)
        # self.constructorLabel = LUILabel(parent=self.constructorParameters, text=u"Additional Constructor Parameters")
        # self.constructorLayout = UIVerticalLayout(parent=self.constructorParameters, spacing=10, use_dividers=True)
        # self.constructorLayout.top = 30

        # Public functions
        self.publicFunctions = LUIFrame(width=340, style=LUIFrame.Sunken)
        self.functionsLabel = LUILabel(parent=self.publicFunctions, text=U"Additional Public functions")
        self.functionsLayout = LUIVerticalLayout(parent=self.publicFunctions,spacing=10, use_dividers=True)
        self.functionsLayout.top = 30

        # Events
        self.events = LUIFrame(width=340,style=LUIFrame.Sunken)
        self.eventsLabel = LUILabel(parent=self.events, text=U"Additional Events")
        self.eventsLayout = LUIVerticalLayout(parent=self.events, spacing=10, use_dividers=True)
        self.eventsLayout.top = 30

        # Actions
        self.actions = LUIFrame(width=340,style=LUIFrame.Sunken, height=80)
        self.actionsLabel = LUILabel(parent=self.actions, text=U"Demo-Actions")
        self.actionsSelect = LUISelectbox(parent=self.actions, width=245, top=30)
        self.actionsBtn = LUIButton(parent=self.actions, right=0, top=30, text=u"Execute", template="ButtonMagic")
        self.actionsBtn.bind("click", self._exec_action)

        self.rightBar.add_row(self.actions)
        # self.rightBar.add_row(self.constructorParameters)
        self.rightBar.add_row(self.publicFunctions)
        self.rightBar.add_row(self.events)

        # Widget
        self.widgetContainer = LUIFrame(parent=self.root, width=360, height=250, style=LUIFrame.Sunken)
        self.widgetLabel = LUILabel(parent=self.widgetContainer, text=u"Widget Demo")
        self.widgetContainer.left = 26
        self.widgetContainer.top = 120

        # Source Code
        self.sourceContainer = LUIFrame(parent=self.root, width=360, height=200, style=LUIFrame.Sunken)
        self.sourceLabel = LUILabel(parent=self.sourceContainer, text=u"Default Constructor")
        self.copyCodeButton = LUIButton(parent=self.sourceContainer,
                text=u"Copy to Clipboard", template="ButtonMagic",
                right=-5, bottom=-5)
        self.sourceContainer.left = 26
        self.sourceContainer.top = 390
        self.sourceContent = LUIObject(self.sourceContainer)
        self.sourceContent.top = 40


        self.widgetNode = LUIObject(self.widgetContainer, x=0, y=40)


    def _exec_action(self, event):
        selected = self.actionsSelect.get_selected_option()
        if selected is not None:
            selected()

    def set_actions(self, actions):
        opts = []

        for name, action in actions.items():
            opts.append((action, name))

        self.actionsSelect.set_options(opts)

    def add_public_function(self, name, parameters=None, return_type="void"):
        label = LUIFormattedLabel()
        label.add_text(text=return_type + " ", color = (102/255.0, 217/255.0, 239/255.0))
        label.add_text(text=name + " ", color = (166/255.0, 226/255.0, 46/255.0))

        label.add_text(text="( ", color=(0.9,0.9,0.9))

        if parameters is not None:
            for index, (pname, ptype) in enumerate(parameters):
                label.add_text(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
                label.add_text(text=" : ", color=(0.9,0.9,0.9))
                label.add_text(text=ptype, color=(102/255.0, 217/255.0, 239/255.0))

                if index < len(parameters) - 1:
                    label.add_text(text=",", color=(0.9,0.9,0.9))
        label.add_text(text=" )", color=(0.9,0.9,0.9))
        self.functionsLayout.add_row(label)
        self.update_layouts()

    def add_constructor_parameter(self, name, default):
        # label = UIFormattedLabel()
        # label.add_text(text=name, color=(255/255.0, 151/255.0, 31/255.0))
        # label.add_text(text=" = ", color=(249/255.0, 38/255.0, 114/255.0))
        # label.add_text(text=default, color=(153/255.0, 129/255.0, 255/255.0))
        # self.constructorLayout.add_row(label)
        self.constructorParams.append((name, default))
        self.update_layouts()

    def add_event(self, event_name):
        label = LUILabel(text=event_name)
        label.color = (1,1,1,0.5)
        self.eventsLayout.add_row(label)
        self.update_layouts()

    def update_layouts(self):
        self.publicFunctions.fit_height_to_children()
        # self.constructorParameters.fit_height_to_children()
        self.events.fit_height_to_children()
        self.rightBar.update()

    def construct_sourcecode(self, classname):
        self.sourceContent.remove_all_children()
        label = LUIFormattedLabel(parent=self.sourceContent)
        label.add_text(text="element ", color=(0.9,0.9,0.9))
        label.add_text(text="= ", color=(249/255.0, 38/255.0, 114/255.0))
        label.add_text(text=classname, color=(166/255.0, 226/255.0, 46/255.0))
        label.add_text(text="(", color=(0.9,0.9,0.9))

        for index, (pname, pvalue) in enumerate(self.constructorParams):
            label.br()
            label.add_text(text=" " * 15)
            label.add_text(text=pname, color=(255/255.0, 151/255.0, 31/255.0))
            label.add_text(text=" = ")
            label.add_text(text=pvalue, color=(153/255.0, 129/255.0, 255/255.0))

            if index < len(self.constructorParams) - 1:
                label.add_text(text=",")

        label.add_text(text=")")

        self.sourceContent.fit_height_to_children()
        self.sourceContainer.fit_height_to_children()
        self.sourceContainer.height += 40


    def get_widget_node(self):
        return self.widgetNode

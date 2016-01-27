
from panda3d.lui import LUIObject, LUISprite
from LUICallback import LUICallback
from LUILabel import LUILabel
from LUILayouts import LUICornerLayout
from LUIInitialState import LUIInitialState

from functools import partial

class LUISelectbox(LUIObject, LUICallback):

    def __init__(self, width=200, options=None, selectedOption=None, **kwargs):
        LUIObject.__init__(self, x=0, y=0, w=width+4, h=0, solid=True)
        LUIInitialState.init(self, kwargs)
        LUICallback.__init__(self)

        # The selectbox has a small border, to correct this we move it
        self.margin_left = -2

        self.bgLeft = LUISprite(self, "Selectbox_Left", "skin")
        self.bgMid = LUISprite(self, "Selectbox", "skin")
        self.bgRight = LUISprite(self, "Selectbox_Right", "skin")

        self.bgMid.width = self.width - self.bgLeft.width - self.bgRight.width
        self.bgMid.left = self.bgLeft.width
        self.bgRight.left = self.bgMid.width + self.bgMid.left

        self.bgRight.z_offset = 1

        self.labelContainer = LUIObject(self, x=10, y=6, w=width - 20 - self.bgRight.width, h=self.bgMid.height - 6)
        self.labelContainer.clip_bounds = (0,0,0,0)

        self.label = LUILabel(parent=self.labelContainer, text=u"Select an option ..", shadow=True)

        self.bgRight.bind("mouseover", self._knob_mouseover)
        self.bgRight.bind("mouseout", self._knob_mouseout)
        self.bgRight.bind("click", self.on_click)
        self.bgRight.bind("click", self.on_click)

        self.fit_to_children()

        self.dropMenu = UISelectdrop(parent=self, width=width)
        self.dropMenu.top = self.bgMid.height - 7
        self.dropMenu.topmost = True

        self.dropOpen = False
        self.dropMenu.hide()

        self.options = []
        self.currentOptionId = None

        if options is not None:
            self.options = options

        self._select_option(selectedOption)

    def get_selected_option(self):
        return self.currentOptionId

    def _render_options(self):
        self.dropMenu._render_options(self.options)

    def set_options(self, options):
        self.options = options
        self.currentOptionId = None
        self._render_options()

    def _select_option(self, optid):
        self.label.color = (1,1,1,1)
        for optID, optVal in self.options:
            if optID == optid:
                self.label.text = optVal
                self.currentOptionId = optID
                return
        self.label.color = (1,1,1,0.5)

    def _knob_mouseover(self, event):
        self.bgRight.color = (0.9,0.9,0.9,1.0)

    def _knob_mouseout(self, event):
        self.bgRight.color = (1,1,1,1.0)

    def on_click(self, event):
        self.request_focus()
        if self.dropOpen:
            self._close_drop()
        else:
            self._open_drop()

    def on_mousedown(self, event):
        self.bgLeft.color = (0.9,0.9,0.9,1.0)
        self.bgMid.color = (0.9,0.9,0.9,1.0)

    def on_mouseup(self, event):
        self.bgLeft.color = (1,1,1,1.0)
        self.bgMid.color = (1,1,1,1.0)

    def _open_drop(self):
        if not self.dropOpen:
            self._render_options()
            self.dropMenu.show()
            self.request_focus()

            self.dropOpen = True

    def _close_drop(self):
        if self.dropOpen:
            self.dropMenu.hide()

            self.dropOpen = False

    def _on_option_selected(self, optid):
        self._select_option(optid)
        self._close_drop()

    def on_blur(self, event):
        self._close_drop()



class UISelectdrop(LUIObject):

    def __init__(self, parent, width=200):
        LUIObject.__init__(self, x=0, y=0, w=width, h=1, solid=True)

        self.layout = LUICornerLayout(parent=self, image_prefix="Selectdrop_", width=width + 10, height=100)
        self.layout.margin_left = -3

        self.opener = LUISprite(self, "SelectboxOpen_Right", "skin")
        self.opener.right = -4
        self.opener.top = -25
        self.opener.z_offset = 3

        self.container = LUIObject(self.layout, 0, 0, 0, 0)
        self.container.width = self.width
        self.container.clip_bounds = (0,0,0,0)
        self.container.left = 5

        self.selectbox = parent
        self.parent = self.selectbox

    def _on_opt_over(self, event):
        event.sender.color = (0,0,0,0.1)

    def _on_opt_out(self, event):
        event.sender.color = (0,0,0,0)

    def _on_opt_click(self, optid, event):
        self.selectbox._on_option_selected(optid)

    def _render_options(self, options):
        visible = min(4, len(options))
        offsetTop = 6
        self.layout.height = visible * 30 + offsetTop + 11
        self.container.height = visible * 30 + offsetTop + 1
        self.layout.update_layout()
        self.container.remove_all_children()
        
        currentY = offsetTop
        for optId, optVal in options:
            optContainer = LUIObject(self.container, x=0, y=currentY, w=self.container.width - 30, h=30)

            optBg = LUISprite(optContainer, "blank", "skin")
            optBg.width = self.container.width
            optBg.height = optContainer.height
            optBg.color = (0,0,0,0)
            optBg.bind("mouseover", self._on_opt_over)
            optBg.bind("mouseout", self._on_opt_out)
            optBg.bind("click", partial(self._on_opt_click, optId))
            optBg.solid = True

            optLabel = LUILabel(parent=optContainer, text=unicode(optVal), shadow=True)
            optLabel.top = 5
            optLabel.left = 8

            if optId == self.selectbox.get_selected_option():
                optLabel.color = (0.6, 0.9, 0.4, 1.0)

            divider = LUISprite(optContainer, "SelectdropDivider", "skin")
            divider.top = 30 - divider.height / 2
            divider.width = self.container.width

            currentY += 30

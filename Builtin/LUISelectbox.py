
from LUIObject import LUIObject
from LUISprite import LUISprite
from LUILabel import LUILabel
from LUILayouts import LUICornerLayout, LUIHorizontalStretchedLayout
from LUIInitialState import LUIInitialState

from functools import partial

__all__ = ["LUISelectbox"]

class LUISelectbox(LUIObject):

    """ Selectbox widget, showing several options whereas the user can select
    only one. """

    def __init__(self, width=200, options=None, selected_option=None, **kwargs):
        """ Constructs a new selectbox with a given width """
        LUIObject.__init__(self, x=0, y=0, w=width+4, solid=True)
        LUIInitialState.init(self, kwargs)

        # The selectbox has a small border, to correct this we move it
        self.margin.left = -2

        self._bg_layout = LUIHorizontalStretchedLayout(parent=self, prefix="Selectbox", width="100%")

        self._label_container = LUIObject(self, x=10, y=0)
        self._label_container.set_size("100%", "100%")
        self._label_container.clip_bounds = (0,0,0,0)
        self._label = LUILabel(parent=self._label_container, text=u"Select an option ..")
        self._label.center_vertical = True

        self._drop_menu = LUISelectdrop(parent=self, width=width)
        self._drop_menu.top = self._bg_layout._sprite_right.height - 7
        self._drop_menu.topmost = True

        self._drop_open = False
        self._drop_menu.hide()

        self._options = []
        self._current_option_id = None

        if options is not None:
            self._options = options

        self._select_option(selected_option)

    def get_selected_option(self):
        """ Returns the selected option """
        return self._current_option_id

    def set_selected_option(self, option_id):
        """ Sets the selected option """
        raise NotImplementedError()

    selected_option = property(get_selected_option, set_selected_option)

    def _render_options(self):
        """ Internal method to render all available options """
        self._drop_menu._render_options(self._options)

    def get_options(self):
        """ Returns the list of options """
        return self._options

    def set_options(self, options):
        """ Sets the list of options, options should be a list containing entries
        whereas each entry is a tuple in the format (option_id, option_label).
        The option ID can be an arbitrary object, and will not get modified. """
        self._options = options
        self._current_option_id = None
        self._render_options()

    options = property(get_options, set_options)

    def _select_option(self, opt_id):
        """ Internal method to select an option """
        self._label.alpha = 1.0
        for elem_opt_id, opt_val in self._options:
            if opt_id == elem_opt_id:
                self._label.text = opt_val
                self._current_option_id = opt_id
                return
        self._label.alpha = 0.3

    # def on_mouseover(self, event):
    #     """ Internal handle when the select-knob was hovered """
    #     self._bg_layout.color = (0.9,0.9,0.9,1.0)

    # def on_mouseout(self, event):
    #     """ Internal handle when the select-knob was no longer hovered """
    #     self._bg_layout.color = (1,1,1,1.0)

    def on_click(self, event):
        """ On-Click handler """
        self.request_focus()
        if self._drop_open:
            self._close_drop()
        else:
            self._open_drop()

    def on_mousedown(self, event):
        """ Mousedown handler """
        self._bg_layout.alpha = 0.9

    def on_mouseup(self, event):
        """ Mouseup handler """
        self._bg_layout.alpha = 1

    def on_blur(self, event):
        """ Internal handler when the selectbox lost focus """
        if not self._drop_menu.focused:
            self._close_drop()

    def _open_drop(self):
        """ Internal method to show the dropdown menu """
        if not self._drop_open:
            self._render_options()
            self._drop_menu.show()
            self.request_focus()
            self._drop_open = True

    def _close_drop(self):
        """ Internal method to close the dropdown menu """
        if self._drop_open:
            self._drop_menu.hide()
            self._drop_open = False

    def _on_option_selected(self, opt_id):
        """ Internal method when an option got selected """
        self._select_option(opt_id)
        self._close_drop()


class LUISelectdrop(LUIObject):

    """ Internal class used by the selectbox, representing the dropdown menu """

    def __init__(self, parent, width=200):
        LUIObject.__init__(self, x=0, y=0, w=width, h=1, solid=True)

        self._layout = LUICornerLayout(parent=self, image_prefix="Selectdrop_",
                                       width=width + 10, height=100)
        self._layout.margin.left = -3

        self._opener = LUISprite(self, "SelectboxOpen_Right", "skin")
        self._opener.right = -4
        self._opener.top = -25
        self._opener.z_offset = 3

        self._container = LUIObject(self._layout, 0, 0, 0, 0)
        self._container.width = self.width
        self._container.clip_bounds = (0,0,0,0)
        self._container.left = 5
        self._container.solid = True
        self._container.bind("mousedown", lambda *args: self.request_focus())

        self._selectbox = parent
        self._option_focus = False
        self.parent = self._selectbox

    def _on_opt_over(self, event):
        """ Inernal handler when an option got hovered """
        event.sender.color = (0,0,0,0.1)

    def _on_opt_out(self, event):
        """ Inernal handler when an option got no longer hovered """
        event.sender.color = (0,0,0,0)

    def _on_opt_click(self, opt_id, event):
        """ Internal handler when an option got clicked """
        self._selectbox._on_option_selected(opt_id)

    def _render_options(self, options):
        """ Internal method to update the options """
        num_visible_options = min(30, len(options))
        offset_top = 6
        self._layout.height = num_visible_options * 30 + offset_top + 11
        self._container.height = num_visible_options * 30 + offset_top + 1
        self._container.remove_all_children()

        current_y = offset_top
        for opt_id, opt_val in options:
            opt_container = LUIObject(self._container, x=0, y=current_y, w=self._container.width - 30, h=30)

            opt_bg = LUISprite(opt_container, "blank", "skin")
            opt_bg.width = self._container.width
            opt_bg.height = opt_container.height
            opt_bg.color = (0,0,0,0)
            opt_bg.bind("mouseover", self._on_opt_over)
            opt_bg.bind("mouseout", self._on_opt_out)
            opt_bg.bind("mousedown", lambda *args: self.request_focus())
            opt_bg.bind("click", partial(self._on_opt_click, opt_id))
            opt_bg.solid = True

            opt_label = LUILabel(parent=opt_container, text=opt_val.encode('utf-8'))
            opt_label.top = 8
            opt_label.left = 8

            if opt_id == self._selectbox.selected_option:
                opt_label.color = (0.6, 0.9, 0.4, 1.0)

            divider = LUISprite(opt_container, "SelectdropDivider", "skin")
            divider.top = 30 - divider.height / 2
            divider.width = self._container.width

            current_y += 30

from LUIFrame import LUIFrame
from LUILabel import LUILabel
from LUIObject import LUIObject
from LUIVerticalLayout import LUIVerticalLayout
from LUIHorizontalLayout import LUIHorizontalLayout

class LUITabbedFrame(LUIFrame):
    def __init__(self, **kwargs):
        super(LUITabbedFrame, self).__init__(**kwargs)

        # The main window layout
        bar_spacing = kwargs.get('bar_spacing', 3)
        self.root_layout = LUIVerticalLayout(parent = self,
                                             spacing = bar_spacing)
        self.root_layout.height = "100%"
        self.root_layout.width = "100%"
        self.root_layout.margin = 0

        # The header bar
        header_spacing = kwargs.get('header_spacing', 3)
        self.header_bar = LUIHorizontalLayout(parent = self.root_layout.cell("?"),
                                              spacing = header_spacing)
        self.root_layout.add(self.header_bar, "?")
        self.header_to_frame = {}
        self.current_frame = None

        # The main window contents        
        self.main_frame = LUIObject()
        self.main_frame.height = "100%"
        self.main_frame.width = "100%"
        self.main_frame.margin = 0
        # self.main_frame.padding = 0
        self.root_layout.add(self.main_frame, "*")
        self.bind("expose", self.on_expose)
        self.bind("unexpose", self.on_unexpose)

    def add(self, header, frame):
        # header
        if isinstance(header, str):
            header = LUILabel(text = header)
        self.header_bar.add(header, "?")
        self.header_to_frame[header] = frame
        header.solid = True
        header.bind("click", self._change_to_tab)
        # Frame
        frame.parent = self.main_frame
        frame.width = "100%"
        frame.height = "100%"
        # Put frame in front
        if self.current_frame is None:
            self.current_frame = frame
            self.current_frame.show()
        else:
            frame.hide()
        return header

    def _find_header_index(self, header):
        for idx, child in enumerate(self.header_bar.children):
            if any([grandchild == header for grandchild in child.children]):
                break
        else:
            raise ValueError("Given object is not a header bar item.")
        return idx

    def remove(self, header):
        idx = self._find_header_index(header)
        self.header_bar.remove_cell(idx)
        frame = self.header_to_frame[header]
        frame.parent = None
        del self.header_to_frame[header]
        if self.current_frame == frame:
            self.current_frame = None

    def _change_to_tab(self, lui_event):
        header = lui_event.sender
        if self.current_frame is not None:
            self.current_frame.trigger_event("unexpose")
            self.current_frame.hide()
        self.current_frame = self.header_to_frame[header]
        self.current_frame.show()
        self.current_frame.trigger_event("expose")

    def on_expose(self, event):
        self.current_frame.trigger_event("expose")

    def on_unexpose(self, event):
        self.current_frame.trigger_event("unexpose")

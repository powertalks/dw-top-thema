from tkinter import X, BOTH, Frame, GROOVE

from gui.status.status_panel import StatusPanel
from gui.content.content_panel import ContentPanel
from gui.title.title_panel import TitlePanel


class MainPanel(Frame):

    def __init__(self, master, title):
        super().__init__(master)
        self.title = title
        self.content_panel = None
        self.status_panel = None
        self.build_components()

    def build_components(self):
        self.build_title_panel()
        self.build_cotent_panel()
        self.build_status_panel()

    def build_title_panel(self):
        panel = TitlePanel(self, self.title)
        panel.pack(fill=X, padx=0, pady=0)

    def build_cotent_panel(self):
        self.content_panel = ContentPanel(self)
        self.content_panel.pack(fill=BOTH, expand=1, ipadx=0, ipady=0, padx=0, pady=0)

    def build_status_panel(self):
        self.status_panel = StatusPanel(self)
        self.status_panel.config(relief=GROOVE, borderwidth=2)
        self.status_panel.pack(fill=X, ipadx=2, ipady=2, padx=0, pady=0)

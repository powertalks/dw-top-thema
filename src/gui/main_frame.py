from tkinter import BOTH, Frame, FLAT

from gui.main_panel import MainPanel


class MainFrame(Frame):

    def __init__(self, master, title):
        super().__init__(master)
        self.title = title
        self.main_panel = None
        self.build_components()

    def build_components(self):
        self.main_panel = MainPanel(self, self.title)
        self.main_panel.config(relief=FLAT)
        self.main_panel.config(borderwidth=0)
        self.main_panel.pack(fill=BOTH, expand=1, padx=0, pady=0, ipadx=0, ipady=0)

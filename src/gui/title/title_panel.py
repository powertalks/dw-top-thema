from tkinter import Frame, Label, BOTH, LEFT, PhotoImage


class TitlePanel(Frame):

    def __init__(self, master, title):
        super().__init__(master)
        self.title = title
        self.text_label = None
        self.img_label = None
        self.description_label = None
        self.build_components()
        self.config(bg="white")

    def build_components(self):
        img = PhotoImage(file="../img/download.png")
        self.img_label = Label(self, image=img)
        self.img_label.image = img

        self.text_label = Label(self, text=self.title, font="Helvetica 18 bold")
        self.text_label["compound"] = LEFT
        self.text_label["image"] = img
        self.text_label.config(bg="#e0e0e0")
        self.text_label.config(padx=20, pady=20)
        self.text_label.pack(fill=BOTH, expand=1, side=LEFT)

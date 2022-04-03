import time
import threading
from datetime import datetime

from tkinter import LEFT, FLAT, X, CENTER, StringVar
from tkinter.ttk import Frame, Label

from backend.control.util.log_util import log_error


class StatusPanel(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.type_font = "Arial 10 bold"
        self.label_font = "Arial 10"

        # The status bar is also used to display tooltips for widgets. When the mouse hovering happens to one
        # widget, the widget's tooltip should be displayed in the status bar. When the mouse leaves the widget,
        # the last status message should be displayed.
        self.last_message_type = ""
        self.last_message_text = ""
        self.is_tooltip_enabled = True

        self.type_var = StringVar()
        self.text_var = StringVar()
        self.time_var = StringVar()

        self.type_label = None
        self.text_label = None
        self.time_label = None

        self.build_components()

        self.is_timer_to_stop = False
        self.start_timer_thread()

    def build_components(self):
        ipadx_val = 20
        ipady_val = 3

        self.type_label = Label(self, text="INFO", textvariable=self.type_var)
        self.type_label.config(anchor=CENTER, font=self.label_font)
        self.type_label.config(relief=FLAT)
        self.type_label.config(borderwidth=2)
        self.type_label.pack(side=LEFT, ipadx=ipadx_val, ipady=ipady_val)

        self.text_label = Label(self, text="Ready", textvariable=self.text_var)
        self.text_label.config(anchor=CENTER, font=self.label_font)
        self.text_label.config(relief=FLAT)
        self.text_label.config(borderwidth=2)
        self.text_label.pack(side=LEFT, fill=X, expand=1, ipadx=ipadx_val, ipady=ipady_val)

        self.time_label = Label(self, text="2022/03/15 21:50:20", textvariable=self.time_var)
        self.time_label.config(anchor=CENTER, font=self.label_font)
        self.time_label.config(width=20)
        self.time_label.config(relief=FLAT)
        self.time_label.config(borderwidth=2)
        self.time_label.pack(side=LEFT, ipadx=ipadx_val, ipady=ipady_val)

        self.type_label.config(background="SystemButtonFace")
        self.text_label.config(background="SystemButtonFace")
        self.time_label.config(background="SystemButtonFace")

    def status_error(self, msg):
        self.last_message_type = "error"
        self.last_message_text = msg
        self.show_error(msg)

    def status_warning(self, msg):
        self.last_message_type = "warning"
        self.last_message_text = msg
        self.show_warning(msg)

    def status_info(self, msg):
        self.last_message_type = "info"
        self.last_message_text = msg
        self.show_info(msg)

    def disable_tooltips(self):
        self.is_tooltip_enabled = False

    def enable_tooltips(self):
        self.is_tooltip_enabled = True

    def status_info_without_stack(self, msg):
        if not self.is_tooltip_enabled:
            return
        self.text_label.config(background="SystemButtonFace")
        self.type_var.set("")
        msg = trim_message(msg)
        self.text_var.set(msg)

    def restore_last_message(self):
        if "error" == self.last_message_type:
            self.show_error(self.last_message_text)
        elif "warning" == self.last_message_type:
            self.show_warning(self.last_message_text)
        elif "error" == self.last_message_type:
            self.show_info(self.last_message_text)
        else:
            self.show_info("Ready.")

    def show_error(self, msg):
        self.text_label.config(background="#fe2712")
        self.type_var.set("ERROR")
        msg = trim_message(msg)
        self.text_var.set(msg)

    def show_warning(self, msg):
        self.text_label.config(background="#b2d732")
        self.type_var.set("WARNING")
        msg = trim_message(msg)
        self.text_var.set(msg)

    def show_info(self, msg):
        self.text_label.config(background="SystemButtonFace")
        self.type_var.set("INFO")
        msg = trim_message(msg)
        self.text_var.set(msg)

    def start_timer_thread(self):
        th = threading.Thread(target=self.update_time)
        th.start()

    def update_time(self):
        while not self.is_timer_to_stop:
            txt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            try:
                # When the application is terminated, this line will trigger a RuntimeError.
                self.time_var.set(txt)
                time.sleep(1)
            except RuntimeError as ex:
                log_error("Timer stopped due to exception. Reason: {}".format(str(ex)))
                break


def trim_message(msg):
    if len(msg) > 80:
        msg = msg[0:50] + "..." + msg[-30:]
    return msg

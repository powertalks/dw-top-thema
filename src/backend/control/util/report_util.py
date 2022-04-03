import sys
from tkinter import messagebox
from tkinter.messagebox import OKCANCEL

from main.global_vars import g_app_name, destroy_main_window


def show_error(msg):
    val = messagebox.showerror(title=g_app_name, message=msg, type=OKCANCEL)
    if "cancel" == val:
        destroy_main_window()
        sys.exit(1)

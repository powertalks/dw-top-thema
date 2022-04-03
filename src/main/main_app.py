from tkinter import Tk, BOTH

from gui.main_frame import MainFrame
from main.global_vars import set_main_window, get_main_window, destroy_main_window, g_app_title, status_info, \
    on_alt_d_pressed, on_alt_s_pressed


def show_main_window():
    create_main_window()
    create_main_frame()
    get_main_window().mainloop()


def create_main_window():
    main_window = Tk()
    main_window.title(g_app_title)

    # Initial size and initial position.
    main_window.geometry("900x600+100+100")

    # Bind the Windows message with a function.
    main_window.protocol("WM_DELETE_WINDOW", lambda: destroy_main_window())

    # Bind the key "alt + d" with a function.
    main_window.bind("<Alt_L><d>", lambda e: on_alt_d_pressed())
    main_window.bind("<Alt_L><q>", lambda e: destroy_main_window())
    main_window.bind("<Alt_L><s>", lambda e: on_alt_s_pressed())

    set_main_window(main_window)


def create_main_frame():
    main_window = get_main_window()
    main_frame = MainFrame(main_window, g_app_title)
    main_frame.pack(fill=BOTH, expand=1)
    status_info("Ready.")


if __name__ == '__main__':
    show_main_window()
    # run_unit_tests()

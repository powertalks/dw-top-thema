from tkinter import filedialog

g_main_window = None

g_app_name = "DWTT"
g_app_title = "Deutsche Welle Top Thema Downloader"

g_start_url = "https://www.dw.com/de/top-thema/s-8031"
g_url_prefix1 = "https://www.dw.com"
g_url_prefix2 = "https://learngerman.dw.com"

g_date_format = "%Y-%m-%d"

g_in_test = True


def set_main_window(obj):
    global g_main_window
    g_main_window = obj


def get_main_window():
    return g_main_window


def destroy_main_window():
    global g_main_window
    if g_main_window is not None:
        if "!mainframe" in g_main_window.children:
            main_frame = g_main_window.children["!mainframe"]
            if main_frame is not None:
                main_frame.main_panel.status_panel.is_timer_to_stop = True
        g_main_window.destroy()


def on_alt_d_pressed():
    main_frame = get_main_window().children["!mainframe"]
    main_frame.main_panel.content_panel.execute_download()


def on_alt_s_pressed():
    main_frame = get_main_window().children["!mainframe"]
    main_frame.main_panel.content_panel.select_output_dir()


def is_manuscript_selected():
    if g_in_test:
        return True
    main_frame = get_main_window().children["!mainframe"]
    return main_frame.main_panel.content_panel.is_manuscript_selected()


def is_exercise_selected():
    if g_in_test:
        return True
    main_frame = get_main_window().children["!mainframe"]
    return main_frame.main_panel.content_panel.is_exercise_selected()


def is_audio_selected():
    if g_in_test:
        return True
    main_frame = get_main_window().children["!mainframe"]
    return main_frame.main_panel.content_panel.is_audio_selected()


def select_dir():
    path = filedialog.askdirectory(title=g_app_name + "Select Directory")
    return path


def status_error(msg):
    if g_in_test:
        return
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.status_error(msg)


def status_warning(msg):
    if g_in_test:
        return
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.status_warning(msg)


def status_info(msg):
    if g_in_test:
        return
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.status_info(msg)


def status_info_without_stack(msg):
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.status_info_without_stack(msg)


def status_bar_restore_last_message():
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.restore_last_message()


def disable_tooltips():
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.disable_tooltips()


def enable_tooltips():
    main_frame = g_main_window.children["!mainframe"]
    main_frame.main_panel.status_panel.enable_tooltips()


def get_url_prefix(year):
    val = int(year)
    if val < 2021:
        return g_url_prefix1
    else:
        return g_url_prefix2

import os
import threading
import webbrowser
from os.path import expanduser
from tkinter import Frame, Label, Entry, GROOVE, W, StringVar, Checkbutton, LEFT, IntVar, Button, RIDGE, E, X
from tkinter.ttk import Combobox

from backend.control.web_page.download_worker import DownloadWorker
from main.global_vars import destroy_main_window, select_dir, g_start_url, status_info, status_error, \
    status_info_without_stack, status_bar_restore_last_message, disable_tooltips, enable_tooltips

g_button_width = 15
g_button_relief = GROOVE


class ContentPanel(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.label_font = ("Arial", 10, "bold")
        self.input_font = ("Arial", 10, "normal")
        self.description_font = ("Arial", 10, "normal")
        self.hyperlink_font = ("Arial", 10, "normal")
        self.internal_padx = 10
        self.internal_pady = 3

        self.description_label = None
        self.hyperlink_label = None

        self.archive_url_entry = None
        self.year_combo_box = None
        self.manuscript_check_box = None
        self.exercise_check_box = None
        self.audio_check_box = None
        self.output_dir_entry = None

        # Variables for each input widgets.
        self.archive_url_value = StringVar()
        self.manuscript_selection_value = IntVar()
        self.exercise_selection_value = IntVar()
        self.audio_selection_value = IntVar()
        self.year_value = StringVar()
        self.output_dir_value = StringVar()

        # Set the initial value for some widget variables.
        self.manuscript_selection_value.set(1)
        self.exercise_selection_value.set(1)
        self.audio_selection_value.set(1)
        self.output_dir_value.set(os.path.join(expanduser("~"), "dw"))

        self.build_components()

    def build_components(self):
        area_container = Frame(self)
        area_container.pack(padx=20, pady=20, ipadx=0, ipady=0)

        self.create_description_area(area_container)
        self.create_input_area(area_container)

    def create_description_area(self, parent_container):
        panel = Frame(parent_container)
        panel.pack(padx=20, pady=10, ipadx=0, ipady=0)

        desc = "\"Top-Thema\" is a channel in Deutsche Welle to provide the learning material in the B1 level."
        description_label = Label(panel, text=desc, font=self.description_font)
        description_label.pack(fill=X, expand=1)

        archives_url_label = Label(panel, text=g_start_url, font=self.hyperlink_font, cursor="hand2")
        archives_url_label.config(fg="blue")
        archives_url_label.bind("<Button-1>", lambda evt: open_in_browser(g_start_url))
        archives_url_label.pack()

    def create_input_area(self, parent_container):
        content_frame = Frame(parent_container)
        content_frame.config(relief=RIDGE, borderwidth=2)
        content_frame.pack(padx=20, pady=20, ipadx=0, ipady=0)

        input_frame = Frame(content_frame)
        input_frame.pack(padx=20, pady=20, ipadx=0, ipady=0)

        row = 0
        self.create_archive_url_row(input_frame, row)
        row += 1
        self.create_year_row(input_frame, row)
        row += 1
        self.create_file_type_selection_row(input_frame, row)
        row += 1
        self.create_output_dir_row(input_frame, row)
        row += 1
        self.create_button_row(input_frame, row)

    def create_archive_url_row(self, container, row_idx):
        label = Label(container, text="Archives' URL:", font=self.label_font)
        label.grid(row=row_idx, column=0, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        self.archive_url_entry = Entry(container, width=60, textvariable=self.archive_url_value, font=self.input_font)
        self.archive_url_entry.config(borderwidth=0)
        self.archive_url_entry.insert(0, g_start_url)
        self.archive_url_entry.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "The URL of the archives' page, if it is changed."))
        self.archive_url_entry.bind("<Leave>", restore_status_bar)
        self.archive_url_entry.grid(row=row_idx, column=1, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

    def create_year_row(self, container, row_idx):
        label = Label(container, text="Year:", font=self.label_font)
        label.grid(row=row_idx, column=0, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        self.year_combo_box = Combobox(container, width=6, textvariable=self.year_value, font=self.input_font)
        self.year_combo_box["values"] = (
            2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)
        self.year_combo_box["state"] = "readonly"
        self.year_combo_box.set("2008")
        self.year_combo_box.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "You may attachment the learning material of the specified year."))
        self.year_combo_box.bind("<Leave>", restore_status_bar)
        self.year_combo_box.grid(row=row_idx, column=1, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

    def create_file_type_selection_row(self, container, row_idx):
        label = Label(container, text="Content:", font=self.label_font)
        label.grid(row=row_idx, column=0, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        panel = Frame(container)
        panel.grid(row=row_idx, column=1, columnspan=2, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        self.manuscript_check_box = Checkbutton(panel, text="Manuscripts", variable=self.manuscript_selection_value)
        self.manuscript_check_box.config(font=self.input_font)
        self.manuscript_check_box.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "If selected, the program will attachment the manuscripts in the PDF format."))
        self.manuscript_check_box.bind("<Leave>", restore_status_bar)
        self.manuscript_check_box.pack(side=LEFT, padx=0)

        self.exercise_check_box = Checkbutton(panel, text="Exercises", variable=self.exercise_selection_value)
        self.exercise_check_box.config(font=self.input_font)
        self.exercise_check_box.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "If selected, the program will attachment the exercises in the PDF format."))
        self.exercise_check_box.bind("<Leave>", restore_status_bar)
        self.exercise_check_box.pack(side=LEFT, padx=20)

        self.audio_check_box = Checkbutton(panel, text="Audios", variable=self.audio_selection_value)
        self.audio_check_box.config(font=self.input_font)
        self.audio_check_box.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "If selected, the program will attachment the audio files in the mp3 format."))
        self.audio_check_box.bind("<Leave>", restore_status_bar)
        self.audio_check_box.pack(side=LEFT, padx=20)

    def create_output_dir_row(self, container, row_idx):
        label = Label(container, text="Output Directory:", font=self.label_font)
        label.grid(row=row_idx, column=0, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        self.output_dir_entry = Entry(container, width=60, textvariable=self.output_dir_value, font=self.input_font)
        self.output_dir_entry.config(borderwidth=0)
        self.output_dir_entry.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "Output directory where the learning material should be saved."))
        self.output_dir_entry.bind("<Leave>", restore_status_bar)
        self.output_dir_entry.grid(row=row_idx, column=1, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

        select_output_dir_button = Button(container, text="Select ...", command=self.select_output_dir, underline=0)
        select_output_dir_button.config(width=g_button_width)
        select_output_dir_button.config(relief=g_button_relief)
        select_output_dir_button.bind("<Enter>", lambda evt: show_tooltip_in_status_bar(
            "Select the output directory where the learning material should be saved."))
        select_output_dir_button.bind("<Leave>", restore_status_bar)
        select_output_dir_button.grid(row=row_idx, column=2, sticky=W, padx=self.internal_padx, pady=self.internal_pady)

    def create_button_row(self, container, row_idx):
        row_frame = Frame(container)
        row_frame.config(relief=RIDGE)
        row_frame.grid(row=row_idx, column=0, columnspan=3, sticky=W + E, padx=self.internal_padx,
                       pady=self.internal_pady)

        alignment_frame = Frame(row_frame)
        alignment_frame.pack()

        download_button = Button(alignment_frame, text="Download", command=self.execute_download, underline=0)
        download_button.config(width=g_button_width)
        download_button.config(relief=g_button_relief)
        download_button.bind("<Enter>", lambda evt: show_tooltip_in_status_bar("Start downloading."))
        download_button.bind("<Leave>", restore_status_bar)
        download_button.grid(row=0, column=0, padx=self.internal_padx, pady=self.internal_pady)

        quit_button = Button(alignment_frame, text="Quit", command=self.execute_quit, underline=0)
        quit_button.config(width=g_button_width)
        quit_button.config(relief=g_button_relief)
        quit_button.bind("<Enter>", lambda evt: show_tooltip_in_status_bar("Terminate the program."))
        quit_button.bind("<Leave>", restore_status_bar)
        quit_button.grid(row=0, column=1, padx=self.internal_padx, pady=self.internal_pady)

    def select_output_dir(self):
        status_info("Select the output directory...")
        dir_path = select_dir()
        if len(dir_path.strip()) > 0:
            self.output_dir_value.set(dir_path)
            status_info("Output directory changed.")
        else:
            status_info("Output directory unchanged.")

    def execute_download(self):
        # Use a thread to execute the attachment, in order to make the main GUI responsive during attachment.
        th = threading.Thread(target=thread_func_of_download, args=(self,))
        th.start()

    def execute_quit(self):
        self.master.status_panel.is_timer_to_stop = True
        destroy_main_window()

    def is_manuscript_selected(self):
        return 1 == self.manuscript_selection_value.get()

    def is_exercise_selected(self):
        return 1 == self.exercise_selection_value.get()

    def is_audio_selected(self):
        return 1 == self.audio_selection_value.get()


def thread_func_of_download(content_panel):
    disable_tooltips()
    worker = DownloadWorker()

    worker.archive_url = content_panel.archive_url_value.get()
    worker.year = content_panel.year_value.get()
    worker.output_dir = content_panel.output_dir_value.get()

    if content_panel.manuscript_selection_value.get() > 0:
        worker.manuscript_files_selected = True
    if content_panel.audio_selection_value.get() > 0:
        worker.audio_files_selected = True

    stat = worker.execute()
    if stat:
        status_info("Download finished successfully.")
    else:
        status_error("Download finished with errors. Please check the log file!")
    enable_tooltips()


def open_in_browser(url):
    webbrowser.open_new(url)


def show_tooltip_in_status_bar(msg):
    status_info_without_stack(msg)


def restore_status_bar(evt):
    status_bar_restore_last_message()

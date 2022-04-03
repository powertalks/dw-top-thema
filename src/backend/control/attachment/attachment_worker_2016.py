import os

from backend.control.attachment.attachment_worker import AttachmentWorker
from backend.control.util.file_system_util import build_file_path
from backend.control.util.http_util import download_pdf, download_mp3
from backend.control.util.log_util import log_error
from main.global_vars import g_date_format


class AttachmentWorker2016(AttachmentWorker):

    def __init__(self):
        super().__init__()

    def fetch_manuscript(self):
        file_path = self.fetch_pdf("manuscript")
        if len(file_path) > 0:
            self.article_info.manuscript_file_path = file_path
            return True
        else:
            return False

    def fetch_exercise(self):
        file_path = self.fetch_pdf("exercise")
        if len(file_path) > 0:
            self.article_info.exercise_file_path = file_path
            return True
        else:
            return False

    def fetch_pdf(self, file_type=""):
        # "file_type" is used to identify "manuscript" from "exercise".
        # Since 2016.07.12, the article web page changes its format. Before that date, manuscript and exercise are
        # saved together in a PDF file. After that date, they are saved separately in two PDF files.
        try:
            dt = self.article_info.date
            web_file = self.article_info.file_path
            file_path = build_file_path(self.output_dir, dt, web_file, file_type, "pdf")
            if os.path.exists(file_path):
                return file_path

            if "manuscript" == file_type:
                url = self.article_info.manuscript_pdf_url
            elif "exercise" == file_type:
                url = self.article_info.exercise_pdf_url
            else:
                log_error("Invalid file type \"{}\" for PDF downloading!".format(file_type))
                return ""

            if download_pdf(url, file_path):
                return file_path
            else:
                log_error("Failed to download the PDF for \"{}\" with type \"{}\"!"
                          .format(self.article_info.date.strftime(g_date_format), file_type))
                return ""
        except Exception as ex:
            log_error("Unexpected: failed to download the manuscript PDF for file \"{}\"! Reason: {}".format(
                self.article_info.file_path, str(ex)))
            return ""

    def fetch_audio(self):
        try:
            dt = self.article_info.date
            web_file = self.article_info.file_path
            file_path = build_file_path(self.output_dir, dt, web_file, "", "mp3")
            if os.path.exists(file_path):
                self.article_info.audio_file_path = file_path
                return True

            url = self.article_info.audio_url
            if download_mp3(url, file_path):
                self.article_info.audio_file_path = file_path
                return True
            else:
                log_error("Failed to download the audio file for \"{}\"!"
                          .format(self.article_info.date.strftime(g_date_format)))
                return False
        except Exception as ex:
            log_error("Unexpected: failed to download the audio file for file \"{}\"! Reason: {}".format(
                self.article_info.file_path, str(ex)))
            return False

import os

from backend.control.attachment.attachment_worker import AttachmentWorker
from backend.control.util.file_system_util import build_file_path
from backend.control.util.http_util import download_text, download_mp3, download_pdf
from backend.control.util.log_util import log_error
from backend.control.util.xml_util import get_html_root
from main.global_vars import g_url_prefix1, g_date_format


# Attachment downloader for articles in 2008, 2009, ..., and the articles before 2016.07.12.
class AttachmentWorker2008(AttachmentWorker):

    def __init__(self):
        super().__init__()
        self.extra_web_file = ""

    def fetch_manuscript(self):
        # For year 2008, the manuscript PDF is save in the given ArticleInfo object.
        file_path = self.fetch_pdf()
        if len(file_path) > 0:
            self.article_info.manuscript_file_path = file_path
            return True
        else:
            return False

    def fetch_exercise(self):
        # For year 2008, the exercise is in the same PDF as the manuscript.
        return True

    def fetch_audio(self):
        if len(self.article_info.audio_url) > 0 and self.article_info.audio_url.startswith("http"):
            # For some years like 2016, the audio URL has been parsed from the hidden "input" element in the web page.
            return self.download_audio_file()
        else:
            # For year 2008, the exercise is in the same PDF as the manuscript.
            return self.fetch_with_extra_download()

    def fetch_with_extra_download(self):
        if len(self.article_info.audio_file_path) > 0:
            return True

        # For year 2008, the audio file is in another page.
        if not self.download_extra_page():
            return False

        # Parse the URL of the audio file
        if not self.parse_audio_url():
            return False

        # Download the audio file
        if not self.download_audio_file():
            return False
        return True

    def download_extra_page(self):
        try:
            dt = self.article_info.date
            web_file = self.article_info.file_path
            output_file = build_file_path(self.cache_dir, dt, web_file, "extra", "html")
            if os.path.exists(output_file):
                self.extra_web_file = output_file
                return True

            url = self.article_info.audio_url
            if not url.startswith("http"):
                url = g_url_prefix1 + url

            if download_text(url, output_file):
                self.extra_web_file = output_file
                return True
            else:
                log_error("Failed to download the extra web page for \"{}\"!".format(
                    self.article_info.date.strftime(g_date_format)))
                return False
        except Exception as ex:
            log_error("Unexpected: failed to download the extra page for file \"{}\"! Reason: {}".format(
                self.article_info.file_path, str(ex)))
            return False

    def parse_audio_url(self):
        try:
            html_root = get_html_root(self.extra_web_file)
            anchor_list = html_root.xpath("//a[@target=\"hiddenDownloadIframe\"]")
            if 1 != len(anchor_list):
                log_error("Failed to find the anchor for the audio file in file \"{}\"!".format(self.extra_web_file))
                return False
            url = anchor_list[0].attrib["href"]
            self.article_info.audio_url = url
            return True
        except Exception as ex:
            log_error(
                "Unexpected: failed to parse the audio URL in file \"{}\"! Reason: {}".format(
                    self.extra_web_file, str(ex)))
            return False

    def download_audio_file(self):
        try:
            dt = self.article_info.date
            web_file = self.article_info.file_path
            output_file = build_file_path(self.output_dir, dt, web_file, "", "mp3")
            if os.path.exists(output_file):
                self.article_info.audio_file_path = output_file
                return True

            url = self.article_info.audio_url
            if download_mp3(url, output_file):
                self.article_info.audio_file_path = output_file
                return True
            else:
                log_error("Failed to download mp3 for \"{}\"!".format(self.article_info.date.strftime(g_date_format)))
                return False
        except Exception as ex:
            log_error("Unexpected: failed to download the audio file for file \"{}\"! Reason: {}".format(
                self.article_info.file_path, str(ex)))
            return False

    def fetch_pdf(self):
        # Since 2016.07.12, the article web page changes its format. Before that date, manuscript and exercise are
        # saved together in a PDF file. After that date, they are saved separately in two PDF files.
        try:
            dt = self.article_info.date
            web_file = self.article_info.file_path
            file_path = build_file_path(self.output_dir, dt, web_file, "", "pdf")
            if os.path.exists(file_path):
                return file_path

            url = self.article_info.manuscript_pdf_url
            if not len(url) > 0:
                log_error("Empty URL for the manuscript in file \"{}\"!".format(web_file))
                return ""

            if download_pdf(url, file_path):
                return file_path
            else:
                return ""
        except Exception as ex:
            log_error("Unexpected: failed to download the manuscript PDF for file \"{}\"! Reason: {}".format(
                self.article_info.file_path, str(ex)))
            return ""

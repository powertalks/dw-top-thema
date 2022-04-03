import os

from backend.control.parser.article_web_parser import ArticleWebParser
from backend.control.util.file_system_util import validate_dir, build_file_path
from backend.control.util.http_util import download_text
from backend.control.util.log_util import log_error
from backend.control.util.xml_util import get_html_root
from backend.model.article_info import ArticleInfo
from main.global_vars import g_url_prefix2


class ArticleWebParser2021(ArticleWebParser):

    def __init__(self):
        super().__init__()
        self.extra_web_file = ""

    def parse_article_info(self):
        html_root = get_html_root(self.file_path)
        # For year 2021, the manuscript and the exercise are in the "Extras" tab.
        info = self.parse_with_extra_download(html_root)
        info.audio_url = self.parse_audio_url(html_root)
        info.file_path = self.file_path
        info.date = self.date
        return info

    def parse_with_extra_download(self, html_root):
        if not self.download_extra_page(html_root):
            return None
        return self.parse_extra_page()

    def parse_manuscript_url(self, html_root):
        # This is a virtual function.
        raise NotImplementedError()

    def parse_exercise_url(self, html_root):
        # This is a virtual function.
        raise NotImplementedError()

    def parse_audio_url(self, html_root):
        try:
            source_list = html_root.xpath("//audio[@class=\"video-js vjs-fluid\"]/source")
            if not len(source_list) > 0:
                log_error("Failed to find the audio URL in \"{}\"!".format(html_root.base))
                return ""

            source = source_list[0]
            url = source.attrib["src"]
            url = url.strip()
            if not len(url) > 0:
                log_error("Empty audio URL in \"{}\"!".format(html_root.base))
                return ""
            return url
        except Exception as ex:
            log_error("Unexpected: failed to parse the audio URL from \"{}\"! Reason: {}"
                      .format(html_root.base, str(ex)))
            return ""

    def download_extra_page(self, html_root):
        try:
            dt = self.date
            web_file = html_root.base
            output_dir = os.path.join(self.output_dir, self.year, "attachments")
            if not validate_dir(output_dir):
                return False

            output_file = build_file_path(output_dir, dt, web_file, "extra", "html")
            if os.path.exists(output_file):
                self.extra_web_file = output_file
                return True

            anchor_list = html_root.xpath("//a[@id=\"extras\"]")
            if not len(anchor_list) > 0:
                log_error("Failed to find the link to the extra page in file \"{}\"!".format(web_file))
                return False

            anchor = anchor_list[0]
            url = anchor.attrib["href"]
            url = url.strip()
            if not url.startswith("http"):
                url = g_url_prefix2 + url

            if download_text(url, output_file):
                self.extra_web_file = output_file
                return True
            else:
                log_error("Failed to download the extra page for file \"{}\"!".format(web_file))
                return True
        except Exception as ex:
            log_error("Unexpected: failed to download the extra page in file \"{}\"! Reason: {}"
                      .format(html_root.base, str(ex)))
            return False

    def parse_extra_page(self):
        try:
            html_root = get_html_root(self.extra_web_file)
            anchor_list = html_root.xpath("//p[@class=\"grammarLink\"]/a")
            if not len(anchor_list) > 0:
                log_error("Failed to find the manuscript/exercise URL in \"{}\"!".format(self.extra_web_file))
                return None

            info = ArticleInfo()
            for anchor in anchor_list:
                url = anchor.attrib["href"].strip()
                if url.endswith(".pdf") and "manuskript" in url.lower():
                    info.manuscript_pdf_url = url
                    if parse_finished(info):
                        return info
                    continue
                if url.endswith(".pdf") and "aufgaben" in url.lower():
                    info.exercise_pdf_url = url
                    if parse_finished(info):
                        return info
                    continue
            return info
        except Exception as ex:
            log_error("Unexpected: failed to parse article info in \"{}\"! Reason: {}"
                      .format(self.extra_web_file, str(ex)))
            return None


def parse_finished(article_info):
    return len(article_info.manuscript_pdf_url) > 0 and len(article_info.exercise_pdf_url) > 0

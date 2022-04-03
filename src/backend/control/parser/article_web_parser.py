from backend.control.util.log_util import log_error
from backend.control.util.xml_util import get_html_root
from backend.model.article_info import ArticleInfo


# Base class for article web parsing.
class ArticleWebParser(object):

    def __init__(self):
        self.file_path = ""
        self.date = None
        self.output_dir = ""
        self.year = ""

    def parse_article_info(self):
        html_root = get_html_root(self.file_path)
        info = ArticleInfo()
        info.file_path = self.file_path
        info.date = self.date
        info.manuscript_pdf_url = self.parse_manuscript_url(html_root)
        info.exercise_pdf_url = self.parse_exercise_url(html_root)
        info.audio_url = self.parse_audio_url(html_root)
        return info

    def parse_manuscript_url(self, html_root):
        # This is a virtual function.
        raise NotImplementedError()

    def parse_exercise_url(self, html_root):
        # This is a virtual function.
        raise NotImplementedError()

    def parse_audio_url(self, html_root):
        # This is a virtual function.
        raise NotImplementedError()

    def try_parse_audio_url_from_hidden_input(self, html_root):
        try:
            input_list = html_root.xpath("//input[@name=\"file_name\"]")
            if not len(input_list) > 0:
                return ""

            input_elem = input_list[0]
            url = input_elem.attrib["value"]
            return url.strip()
        except Exception as ex:
            log_error("Unexpected: failed to parse audio url in file \"{}\"! Reason: {}"
                      .format(self.file_path, str(ex)))
            return ""

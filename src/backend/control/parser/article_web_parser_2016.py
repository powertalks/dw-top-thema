from backend.control.parser.article_web_parser import ArticleWebParser
from backend.control.util.http_util import extract_h2_from_anchor_element
from backend.control.util.log_util import log_error


class ArticleWebParser2016(ArticleWebParser):

    def __init__(self):
        super().__init__()

    def parse_manuscript_url(self, html_root):
        try:
            anchor_list = html_root.xpath("//div[@class=\"linkList download\"]/a")
            if not len(anchor_list) > 0:
                log_error("Failed to find anchor element for attachments in file \"{}\"!".format(self.file_path))
                return

            url = ""
            for anchor in anchor_list:
                url = anchor.attrib["href"]
                txt = extract_h2_from_anchor_element(anchor)
                txt = txt.lower()
                url = url.strip().lower()
                if "manuskript" in txt:
                    return url
                elif "manuskript" in url:
                    return url
                else:
                    url = ""

            if not len(url) > 0:
                log_error("Failed to recognize the manuscript URL from the exercise URL!")
                return ""
            else:
                return url
        except Exception as ex:
            log_error("Unexpected: failed to parse manuscript PDF url in file \"{}\"! Reason: {}"
                      .format(self.file_path, str(ex)))
        return ""

    def parse_exercise_url(self, html_root):
        try:
            anchor_list = html_root.xpath("//div[@class=\"linkList download\"]/a")
            if not len(anchor_list) > 0:
                log_error("Failed to find anchor element for attachments in file \"{}\"!".format(self.file_path))
                return

            url = ""
            for anchor in anchor_list:
                url = anchor.attrib["href"]
                txt = extract_h2_from_anchor_element(anchor)
                txt = txt.lower()
                url = url.strip().lower()
                if "aufgabe" in txt:
                    return url
                elif "aufgabe" in url:
                    return url
                else:
                    url = ""

            if not len(url) > 0:
                log_error("Failed to recognize the manuscript URL from the exercise URL!")
                return ""
            else:
                return url
        except Exception as ex:
            log_error("Unexpected: failed to parse exercise PDF url in file \"{}\"! Reason: {}".format(self.file_path,
                                                                                                       str(ex)))
        return ""

    def parse_audio_url(self, html_root):
        return self.try_parse_audio_url_from_hidden_input(html_root)

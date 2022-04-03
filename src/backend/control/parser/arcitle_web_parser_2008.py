from backend.control.parser.article_web_parser import ArticleWebParser
from backend.control.util.log_util import log_warning, log_error


class ArticleWebParser2008(ArticleWebParser):

    def __init__(self):
        super().__init__()

    def parse_manuscript_url(self, html_root):
        try:
            anchor_list = html_root.xpath("//div[@class=\"linkList download\"]/a")
            if not len(anchor_list) > 0:
                # For year 2008, it is possible that there is no PDF link.
                log_warning("No anchor elements for URL to the manuscript PDF! File: {}".format(self.file_path))
            elif 1 == len(anchor_list):
                # For year 2008, there is only one PDF in each article page.
                anchor = anchor_list[0]
                return anchor.attrib["href"].strip()
            else:
                # Some articles in 2016 will trigger this.
                log_error("Unexpected: more urls to the manuscript PDF! File: {}".format(self.file_path))
        except Exception as ex:
            log_error("Unexpected: failed to find the URL to the manuscript PDF in file \"{}\"! Reason: {}".format(
                self.file_path, str(ex)))
        return ""

    def parse_exercise_url(self, html_root):
        # Exercise is in the same PDF as the manuscript.
        return ""

    def parse_audio_url(self, html_root):
        url = self.try_parse_audio_url_from_hidden_input(html_root)
        if len(url) > 0:
            return url

        url = self.try_parse_audio_url_from_overlay_div(html_root)
        return url

    def try_parse_audio_url_from_overlay_div(self, html_root):
        # Another attachment is necessary to obtain the audio URL.
        # Parse the URL to the second attachment.
        try:
            anchor_list = html_root.xpath("//div[@class=\"linkList overlayIcon\"]/a")
            if not len(anchor_list) > 0:
                # For year 2008, it is possible that there is no audio link.
                log_warning("No anchor elements for URL to the audio file! File: {}".format(self.file_path))
            elif 1 == len(anchor_list):
                # For year 2008, there is only one PDF in each article page.
                anchor = anchor_list[0]
                return anchor.attrib["href"].strip()
            else:
                log_warning("Unexpected: more urls to the audio file! File: {}".format(self.file_path))
                anchor = anchor_list[0]
                return anchor.attrib["href"]
        except Exception as ex:
            log_error(
                "Unexpected: failed to find the URL to the audio file in file \"{}\"! Reason: {}"
                    .format(self.file_path, str(ex)))
        return ""

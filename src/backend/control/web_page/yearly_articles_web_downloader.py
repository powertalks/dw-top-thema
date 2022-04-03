import os

from backend.control.util.http_util import download_text
from backend.control.util.log_util import log_error
from backend.control.util.report_util import show_error
from main.global_vars import get_url_prefix


class YearlyArticlesWebDownloader(object):

    def __init__(self, year, output_dir):
        self.year = year
        self.output_dir = output_dir

    def download(self, url_dict):
        try:
            error_exists = False
            for key, url in url_dict.items():
                tmp = url.lower()
                if not tmp.startswith("http://") and not tmp.startswith("https://"):
                    url_prefix = get_url_prefix(self.year)
                    url = url_prefix + url
                file_path = os.path.join(self.output_dir, self.year, key + ".html")
                if os.path.exists(file_path):
                    continue
                stat = download_text(url, file_path)
                if not stat:
                    log_error("Failed to download the archives web page for year {}!".format(self.year))
                    error_exists = True

            if error_exists:
                show_error("There were errors in downloading. Please check the log file!")
                return False
        except Exception as ex:
            show_error("Unexpected: error happens when yearly articles are downloaded! Reason: {}".format(str(ex)))
            return False
        return True

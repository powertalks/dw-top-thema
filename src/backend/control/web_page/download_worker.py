import os

from backend.control.attachment.attachment_worker_factory import AttachmentWorkerFactory
from backend.control.parser.article_web_parser_factory import ArticleWebParserFactory
from backend.control.parser.root_archives_web_parser import RootArchivesWebParser
from backend.control.parser.yearly_archives_web_parser import YearlyArchivesWebParser
from backend.control.util.file_system_util import validate_dir, file_exists, get_file_list
from backend.control.util.http_util import download_text
from backend.control.util.json_util import save_to_json_file, load_from_json_file
from backend.control.util.log_util import log_error, log_info, log_debug
from backend.control.web_page.yearly_articles_web_downloader import YearlyArticlesWebDownloader
from backend.model.article_info import ArticleInfo
from main.global_vars import g_url_prefix1, g_date_format


class DownloadWorker(object):

    def __init__(self):
        self.archive_url = ""
        self.year = ""
        self.manuscript_selection_value = False
        self.audio_files_selected = False
        self.output_dir = ""
        self.cache_dir = ""

        self.archives_web_file = ""
        self.archives_url_file = ""
        self.year_archive_web_file = ""
        self.year_archive_url_file = ""
        self.year_article_dict_file = ""

    def execute(self):
        if not validate_dir(self.output_dir):
            return False

        if not self.prepare_cache_dir():
            return False

        self.initialize_archives_web_file_path()
        self.initialize_archives_url_file_path()
        self.initialize_year_archive_web_file_path()
        self.initialize_year_archive_url_file_path()
        self.initialize_year_article_dict_file_path()

        if not self.download_archives_page():
            return False

        if not self.parse_archives_page():
            return False

        if not self.download_archive_page_with_year():
            return False

        if not self.parse_archive_page_with_year():
            return False

        if not self.download_pages_in_year():
            return False

        if not self.parse_pages_in_year():
            return False

        if not self.download_attachments():
            return False
        return True

    def prepare_cache_dir(self):
        self.cache_dir = os.path.join(self.output_dir, ".cache")
        if not validate_dir(self.cache_dir):
            return False
        return True

    def initialize_archives_web_file_path(self):
        self.archives_web_file = os.path.join(self.cache_dir, "archives.html")

    def initialize_archives_url_file_path(self):
        self.archives_url_file = os.path.join(self.cache_dir, "archives.json")

    def initialize_year_archive_web_file_path(self):
        file_name = "archive-{}.html".format(self.year)
        self.year_archive_web_file = os.path.join(self.cache_dir, file_name)

    def initialize_year_archive_url_file_path(self):
        file_name = "archive-{}.json".format(self.year)
        self.year_archive_url_file = os.path.join(self.cache_dir, file_name)

    def initialize_year_article_dict_file_path(self):
        file_name = "article-dict-{}.json".format(self.year)
        self.year_article_dict_file = os.path.join(self.cache_dir, file_name)

    def download_archives_page(self):
        # Avoid duplicated downloading.
        if file_exists(self.archives_web_file):
            return True
        if not download_text(self.archive_url, self.archives_web_file):
            log_error("Failed to download the archives web!")
        return True

    def parse_archives_page(self):
        # Avoid duplicated parsing.
        if file_exists(self.archives_url_file):
            return True

        ps = RootArchivesWebParser(self.archives_web_file)
        url_dict = ps.extract()
        if url_dict is None:
            return False
        return save_to_json_file(url_dict, self.archives_url_file)

    def download_archive_page_with_year(self):
        # Avoid duplicated downloading.
        if file_exists(self.year_archive_url_file):
            return True

        # Precondition: The URL json file should exists.
        url_dict = load_from_json_file(self.archives_url_file)
        url = url_dict[self.year]
        url = "{}{}".format(g_url_prefix1, url)
        if not download_text(url, self.year_archive_web_file):
            log_error("Failed to download the archive web for year {}!".format(self.year))
            return False
        return True

    def parse_archive_page_with_year(self):
        # Avoid duplicated parsing.
        if file_exists(self.year_archive_url_file):
            return True

        ps = YearlyArchivesWebParser(self.year_archive_web_file)
        url_dict = ps.extract()
        return save_to_json_file(url_dict, self.year_archive_url_file)

    def download_pages_in_year(self):
        log_info("Download article web pages...")
        dir_path = os.path.join(self.cache_dir, self.year)
        if not validate_dir(dir_path):
            return False

        url_dict = load_from_json_file(self.year_archive_url_file)
        downloader = YearlyArticlesWebDownloader(self.year, self.cache_dir)
        return downloader.download(url_dict)

    def parse_pages_in_year(self):
        log_info("Parse article web pages...")
        # Avoid duplicated parsing.
        if file_exists(self.year_article_dict_file):
            return True

        # Parse pdf/mp3 urls from the year folder.
        dict_list = self.parse_article_dict_from_pages_in_year()
        return save_to_json_file(dict_list, self.year_article_dict_file)

    def parse_article_dict_from_pages_in_year(self):
        log_info("Parse article web pages...")
        try:
            dict_list = list()
            dir_path = os.path.join(self.cache_dir, self.year)
            file_list = get_file_list(dir_path, "*.html")
            for file_path in file_list:
                ps = ArticleWebParserFactory.get_article_web_parser(file_path)
                ps.file_path = file_path
                ps.year = self.year
                ps.output_dir = self.cache_dir
                if ps is None:
                    continue
                info = ps.parse_article_info()
                dict_list.append(info.to_dict())
            return dict_list
        except Exception as ex:
            log_error("Failed to parse the material dictionary for year {}! Reason: {}".format(self.year, str(ex)))
            return None

    def download_attachments(self):
        log_info("Download attachments...")
        dir_path = os.path.join(self.cache_dir, self.year, "attachments")
        if not validate_dir(dir_path):
            return False

        dict_list = load_from_json_file(self.year_article_dict_file)
        if dict_list is None:
            return False

        new_dict_list = list()
        result = True
        for dict_obj in dict_list:
            info = ArticleInfo.from_dict(dict_obj)
            worker = AttachmentWorkerFactory.get_attachment_worker(info.date)
            worker.article_info = info
            worker.cache_dir = dir_path
            worker.output_dir = self.output_dir
            log_debug("Download attachments for date: {}, web file: \"{}\"..."
                      .format(info.date.strftime(g_date_format), info.file_path))
            stat = worker.fetch_attachments()
            if not stat:
                result = False
            new_dict_list.append(worker.article_info.to_dict())

        if not save_to_json_file(new_dict_list, self.year_article_dict_file):
            result = False
        return result

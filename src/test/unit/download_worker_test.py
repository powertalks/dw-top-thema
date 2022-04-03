import os
from os.path import expanduser

from backend.control.web_page.download_worker import DownloadWorker
from main.global_vars import g_start_url


def run_download_worker_test_with_year(year):
    worker = DownloadWorker()

    worker.archive_url = g_start_url
    worker.year = year
    worker.output_dir = os.path.join(expanduser("~"), "dw", year)
    # worker.output_dir = os.path.join(r"D:\dev\pycharm\dw-top-thema2\test", "dw", year)
    # worker.output_dir = os.path.join(r"D:\dev\pycharm\dw-top-thema2\data", "dw", year)
    worker.manuscript_files_selected = True
    worker.audio_files_selected = True

    stat = worker.execute()
    if stat:
        print("# info # test success with year {}".format(year))
    else:
        print("# error # test failed with year {}".format(year))


def run_unit_tests():
    run_download_worker_test_with_year("2008")
    run_download_worker_test_with_year("2009")
    run_download_worker_test_with_year("2010")
    run_download_worker_test_with_year("2011")
    run_download_worker_test_with_year("2012")
    run_download_worker_test_with_year("2013")
    run_download_worker_test_with_year("2014")
    run_download_worker_test_with_year("2015")
    run_download_worker_test_with_year("2016")
    run_download_worker_test_with_year("2017")
    run_download_worker_test_with_year("2018")
    run_download_worker_test_with_year("2019")
    run_download_worker_test_with_year("2020")
    run_download_worker_test_with_year("2021")
    run_download_worker_test_with_year("2022")

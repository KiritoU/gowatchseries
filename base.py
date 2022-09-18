import logging

from bs4 import BeautifulSoup


from settings import CONFIG
from helper import helper
from _db import database

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class Crawler:
    def crawl_soup(self, url):
        html = helper.download_url(url)
        if html.status_code == 404:
            return 404

        soup = BeautifulSoup(html.content, "html.parser")

        return soup

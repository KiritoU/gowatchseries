import logging

from time import sleep

from base import Crawler
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def main():
    crawler = Crawler()
    while True:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}/new-release"
        logging.info(f"Getting URL: {url}")

        soup = Crawler().crawl_soup(url)

        if soup != 404:
            crawler.crawl_new_release_with(soup)
            sleep(CONFIG.WAIT_BETWEEN_LATEST)


if __name__ == "__main__":
    main()

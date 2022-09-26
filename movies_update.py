import logging

from time import sleep

from base import Crawler
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def main():
    crawler = Crawler()
    i = 1
    while True:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}/movies?page={i}"
        logging.info(f"Getting URL: {url}")

        try:
            soup = Crawler().crawl_soup(url)

            if soup == 404:
                i = 1
                continue
            else:
                crawler.crawl_movies_on_page_with(soup)
                sleep(CONFIG.WAIT_BETWEEN_ALL)
        except Exception as e:
            pass

        i += 1


if __name__ == "__main__":
    main()

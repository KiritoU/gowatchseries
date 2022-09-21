import logging

from time import sleep

from base import Crawler
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def main():
    crawler = Crawler()
    i = 1
    while True:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}/list?type=2&page={i}"
        logging.info(f"Getting URL: {url}")

        soup = Crawler().crawl_soup(url)

        list_movies = soup.find("div", class_="list_movies")

        if not list_movies:
            i = 1
        else:
            crawler.crawl_series_on_page_with(list_movies)
            sleep(CONFIG.WAIT_BETWEEN_LATEST)
            i += 1


if __name__ == "__main__":
    main()

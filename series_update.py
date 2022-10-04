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

        try:
            soup = Crawler().crawl_soup(url)

            list_movies = soup.find("div", class_="list_movies")
            series = list_movies.find_all("li")
            if not series:
                i = 1
                continue
            else:
                crawler.crawl_series_on_page_with(list_movies)
        except Exception as e:
            pass

        sleep(CONFIG.WAIT_BETWEEN_ALL)

        i += 1


if __name__ == "__main__":
    main()

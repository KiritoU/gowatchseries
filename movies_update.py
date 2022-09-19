from time import sleep

from base import Crawler
from settings import CONFIG


def main():
    crawler = Crawler()
    while True:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}/movies?page=1"
        soup = Crawler().crawl_soup(url)
        if soup == 404:
            return

        crawler.crawl_movies_on_page_with(soup)
        sleep(CONFIG.WAIT_BETWEEN_LATEST)


if __name__ == "__main__":
    main()

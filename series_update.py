from time import sleep

from base import Crawler
from settings import CONFIG


def main():
    crawler = Crawler()
    while True:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}/list?type=2&page=1"
        soup = Crawler().crawl_soup(url)

        list_movies = soup.find("div", class_="list_movies")
        if not list_movies:
            return

        crawler.crawl_series_on_page_with(list_movies)
        sleep(CONFIG.WAIT_BETWEEN_LATEST)


if __name__ == "__main__":
    main()

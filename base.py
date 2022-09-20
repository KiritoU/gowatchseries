import logging

from bs4 import BeautifulSoup
from time import sleep

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

    def get_movie_details(self, href: str) -> dict:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}{href}"
        logging.info(f"Getting {url}")
        soup = Crawler().crawl_soup(url)
        if soup == 404:
            return {}

        detail = soup.find("div", class_="detail")
        if not detail:
            return {}

        return {
            "description": helper.get_description_from(detail),
            "links": helper.get_links_from(detail),
            **helper.get_info_movies(detail),
        }

    def crawl_movies_on_page_with(self, soup: BeautifulSoup) -> dict:
        items = soup.find("ul", class_="listing items")
        if not items:
            return

        items = items.find_all("li")

        try:
            for item in items:
                a_element = item.find("a")
                href = a_element.get("href")
                picture = a_element.find("div", class_="picture").find("img").get("src")
                name = helper.format_text(a_element.find("div", class_="name").text)
                season = helper.format_text(a_element.find("div", class_="season").text)

                movie_details = {
                    "href": href,
                    "name": name,
                    "season": season,
                    "picture": picture,
                }

                movie_details = {**movie_details, **self.get_movie_details(href)}
                print(movie_details)
                helper.insert_movie(movie_details)

        except Exception as e:
            helper.error_log(
                msg=f"Failed to crawl_movies_on_page_with_soup\n{str(item)}\n{e}",
                log_file="movie_page.log",
            )

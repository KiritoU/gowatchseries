import json
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

    def get_movie_details(self, href: str, title: str = "") -> dict:
        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}{href}"
        logging.info(f"Getting {url}")
        soup = Crawler().crawl_soup(url)
        if soup == 404:
            return {}

        detail = soup.find("div", class_="detail")
        if not detail:
            return {}

        return {
            "title": title,
            "description": helper.get_description_from(detail),
            "links": helper.get_links_from(detail),
            **helper.get_info_movies(soup),
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
                helper.insert_movie(movie_details)

        except Exception as e:
            helper.error_log(
                msg=f"Failed to crawl_movies_on_page_with_soup\n{str(item)}\n{e}",
                log_file="movie_page.log",
            )

    def get_serie_details(self, href: str) -> dict:
        res = {
            "title": "",
            "description": "",
            "genre": "",
            "country": "",
            "released": "",
            "trailer": "",
            "picture": "",
            "child_episode": [],
        }

        url = f"{CONFIG.GO_WATCH_SERIES_HOMEPAGE}{href}"
        soup = self.crawl_soup(url)
        if soup == 404:
            return res

        try:
            detail = soup.find("div", class_="detail")
            res["title"] = helper.format_text(detail.find("h1").text)
            picture = soup.find("div", class_="picture").find("img").get("src")
            res["picture"] = picture

            episodes = soup.find_all("li", class_="child_episode")
            for episode in episodes:
                episode_href = episode.find("a").get("href")
                episode_title = episode.find("a").get("title")
                res["child_episode"].append(
                    self.get_movie_details(episode_href, episode_title)
                )

            first_child = res["child_episode"][0]
            res["description"] = first_child["description"]
            res["genre"] = first_child["genre"]
            res["country"] = first_child["country"]
            res["released"] = first_child["released"]
            res["trailer"] = first_child["trailer"]

        except Exception as e:
            helper.error_log(
                f"Failed to get serie details for {href}\n{e}",
                log_file="serie_details.log",
            )

        return res

    def crawl_series_on_page_with(self, list_movies: BeautifulSoup) -> dict:
        series = list_movies.find_all("li")

        try:
            for serie in series:
                href = serie.find("a").get("href")

                serie_details = self.get_serie_details(href)
                helper.insert_serie(serie_details)

        except Exception as e:
            helper.error_log(
                msg=f"Failed to crawl_series_on_page_with_soup\n{str(serie)}\n{e}",
                log_file="serie_page.log",
            )

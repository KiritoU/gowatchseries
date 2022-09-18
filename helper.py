import requests


from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from slugify import slugify


from _db import database


from settings import CONFIG


class Helper:
    def get_header(self):
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E150",  # noqa: E501
            "Accept-Encoding": "gzip, deflate",
            # "Cookie": CONFIG.COOKIE,
            "Cache-Control": "max-age=0",
            "Accept-Language": "vi-VN",
            "Referer": "https://mangabuddy.com/",
        }
        return header

    def error_log(self, msg: str, log_file: str = "failed.log"):
        datetime_msg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Path("log").mkdir(parents=True, exist_ok=True)
        with open(f"log{CONFIG.OS_SLASH}{log_file}", "a") as f:
            print(f"{datetime_msg} LOG:  {msg}\n{'-' * 80}", file=f)

    def download_url(self, url):
        return requests.get(url, headers=self.get_header())

    def format_text(self, text: str) -> str:
        return text.strip().strip("\n")


helper = Helper()

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

    def get_timeupdate(self) -> str:
        # TODO: later
        timeupdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return timeupdate

    def save_thumb(
        self,
        imageUrl: str,
        imageName: str = "0.jpg",
    ) -> str:
        Path(CONFIG.THUMB_SAVE_PATH).mkdir(parents=True, exist_ok=True)
        saveImage = f"{CONFIG.THUMB_SAVE_PATH}/{imageName}"

        isNotSaved = not Path(saveImage).is_file()
        if isNotSaved:
            image = self.download_url(imageUrl)
            with open(saveImage, "wb") as f:
                f.write(image.content)
            isNotSaved = True

        return [saveImage, isNotSaved]

    def insert_thumb(self, thumbUrl: str) -> int:
        thumbName = thumbUrl.split("/")[-1]
        self.save_thumb(thumbUrl, thumbName)
        timeupdate = self.get_timeupdate()
        thumbPostData = (
            0,
            timeupdate,
            timeupdate,
            "",
            thumbName,
            "",
            "inherit",
            "open",
            "closed",
            "",
            thumbName,
            "",
            "",
            timeupdate,
            timeupdate,
            "",
            0,
            "",
            0,
            "attachment",
            "image/png",
            0,
        )

        thumbId = database.insert_into(table="posts", data=thumbPostData)
        database.insert_into(
            table="postmeta",
            data=(thumbId, "_wp_attached_file", f"covers/{thumbName}"),
        )

        return thumbId

    def insert_movie(self, movie_details: dict, post_type: str = "post"):
        isMovieExists = database.select_all_from(
            table="posts", condition=f"post_title='{movie_details['name']}'"
        )
        if isMovieExists:
            return

        thumbId = self.insert_thumb(movie_details["picture"])
        timeupdate = self.get_timeupdate()
        data = (
            0,
            timeupdate,
            timeupdate,
            movie_details["description"],
            movie_details["name"],
            "",
            "publish",
            "open",
            "closed",
            "",
            slugify(movie_details["name"]),
            "",
            "",
            timeupdate,
            timeupdate,
            "",
            0,
            "",
            0,
            post_type,
            "",
            0,
        )
        postId = database.insert_into(table=f"posts", data=data)

        postmetas = [
            (postId, "_thumbnail_id", thumbId),
            (postId, "tw_multi_chap", "0"),
            (postId, "tw_status", "Đang cập nhật"),
            (postId, "post_question_1", ""),
            (postId, "_post_question_1", "field_60092d86e0981"),
            (
                postId,
                "video_link",
                movie_details["links"][0],
            ),
            (postId, "_video_link", "field_601d685ea50eb"),
            (postId, "chat_luong_video", movie_details["season"]),
            (postId, "_chat_luong_video", "field_5ff2f401eac3f"),
            (postId, "country", ""),
            (postId, "_country", "field_60187b7c9c230"),
            (postId, "released", ""),
            (postId, "_released", "field_62e7989914215"),
            (postId, "trailer", ""),
            (postId, "_trailer", "field_62e798d4938b0"),
            (postId, "genre", ""),
            (postId, "_genre", "field_62eb4674d417d"),
            (postId, "film_type", ""),
            (postId, "_film_type", "field_630ecf331b56c"),
            (postId, "_", "field_630ecf4b1b56d"),
            (postId, "post_views_count", "0"),
        ]

        for pmeta in postmetas:
            database.insert_into(
                table="postmeta",
                data=pmeta,
            )

        return postId


helper = Helper()

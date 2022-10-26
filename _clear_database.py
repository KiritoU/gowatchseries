import logging
import os
import shutil

from _db import Database
from settings import CONFIG

database = Database()

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def delete_saved_thumbs():
    files = os.listdir(CONFIG.THUMB_SAVE_PATH)
    for file in files:
        path = f"{CONFIG.THUMB_SAVE_PATH}/{file}"
        if os.path.isfile(path):
            os.remove(path)


def delete_post_with(post_type: str = ""):
    post_ids = database.select_all_from(
        table="posts", condition=f"post_type='{post_type}'"
    )
    post_ids = [x[0] for x in post_ids]

    for post_id in post_ids:
        logging.info(f"Deleting post: {post_id}")
        _thumbnail_id = database.select_all_from(
            table="postmeta",
            condition=f'post_id={post_id} AND meta_key="_thumbnail_id"',
        )
        if _thumbnail_id:
            database.delete_from(
                table="posts",
                condition=f"ID={_thumbnail_id[0][-1]}",
            )

        database.delete_from(
            table="postmeta",
            condition=f'post_id="{post_id}"',
        )

        database.delete_from(
            table="term_relationships",
            condition=f'object_id="{post_id}"',
        )

        database.delete_from(
            table="posts",
            condition=f'ID="{post_id}"',
        )


def main():
    delete_saved_thumbs()

    # query = "SELECT p.ID FROM `ODJiM2_term_relationships` tr, ODJiM2_posts p WHERE p.ID=tr.object_id AND p.post_type='post' AND tr.term_taxonomy_id=13853"
    postTypes = [
        "post",
        "chap",
        "revision",
        # "customize_changeset",
        # "oembed_cache",
        # "acf-field",
        # "acf-field-group",
        # "video",
        # "um_directory",
        # "um_form",
        # "custom_css",
        # "nav_menu_item",
    ]
    for postType in postTypes:
        delete_post_with(post_type=postType)


if __name__ == "__main__":
    main()

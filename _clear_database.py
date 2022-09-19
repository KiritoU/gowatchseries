import os
import shutil

from _db import Database
from settings import CONFIG

database = Database()


def delete_saved_thumbs():
    files = os.listdir(CONFIG.THUMB_SAVE_PATH)
    for file in files:
        path = f"{CONFIG.THUMB_SAVE_PATH}/{file}"
        if os.path.isfile(path):
            os.remove(path)


def main():
    # delete_saved_thumbs()

    query = "SELECT p.ID FROM `ODJiM2_term_relationships` tr, ODJiM2_posts p WHERE p.ID=tr.object_id AND p.post_type='post' AND tr.term_taxonomy_id=13853"
    post_ids = database.select_with(query)
    print(post_ids)
    # post_ids = [x[0] for x in post_ids]

    # for post_id in post_ids:
    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}manga_volumes",
    #         condition=f'post_id="{post_id}"',
    #     )
    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}manga_chapters",
    #         condition=f'post_id="{post_id}"',
    #     )

    #     _thumbnail_id = database.select_all_from(
    #         table=f"{CONFIG.TABLE_PREFIX}postmeta",
    #         condition=f'post_id={post_id} AND meta_key="_thumbnail_id"',
    #     )
    #     if _thumbnail_id:
    #         database.delete_from(
    #             table=f"{CONFIG.TABLE_PREFIX}posts",
    #             condition=f"ID={_thumbnail_id[0][-1]}",
    #         )

    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}postmeta",
    #         condition=f'post_id="{post_id}"',
    #     )

    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}term_relationships",
    #         condition=f'object_id="{post_id}"',
    #     )

    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}posts",
    #         condition=f'ID="{post_id}"',
    #     )

    # term_taxonomies = database.select_all_from(
    #     table=f"{CONFIG.TABLE_PREFIX}term_taxonomy",
    #     condition='taxonomy LIKE "wp-manga%"',
    #     cols="term_taxonomy_id, term_id",
    # )

    # for term_taxonomy in term_taxonomies:
    #     term_taxonomy_id, term_id = term_taxonomy

    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}term_taxonomy",
    #         condition=f"term_taxonomy_id={term_taxonomy_id}",
    #     )

    #     database.delete_from(
    #         table=f"{CONFIG.TABLE_PREFIX}terms",
    #         condition=f"term_id={term_id}",
    #     )


if __name__ == "__main__":
    main()

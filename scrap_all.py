import json
import os
from pathlib import Path
import time

from AniListPy.anilistpy import AniList


DEFAULT_MEDIA_DIR = "./db/anilist_files/"

def run(media_dir:Path,
        media_type="ANIME",
        start_page=1) -> None:

    if not isinstance(media_dir, Path):
        media_dir = Path(media_dir).resolve()
    media_dir.mkdir(parents=True, exist_ok=True)

    page = start_page
    al_client = AniList()

    while True:
        response = al_client.query_page(page_num=page, media_type=media_type)

        for media in response["data"]["Page"]["media"]:
            filename = media_dir / f"{media['id']}.json"

            if filename.exists():
                print('Skipping "{}"'.format(media["title"]["romaji"]))
                continue

            else:
                # if media_type.upper() == "ANIME":
                #     media_full_data = al_client.query_anime_id(media["id"])
                # else:
                #     media_full_data = al_client.query_manga_id(media["id"])
                
                # Wait to prevent hitting rate limit
                time.sleep(1)

                print("{} \t|\t {}".format(media["id"], media["title"]["romaji"]))

            with filename.open("w+", encoding="utf-8") as outfile:
                json.dump(media, outfile, indent=4, ensure_ascii=False)

        # Do not continue if next request will be empty
        if response["data"]["Page"]["pageInfo"]["hasNextPage"] == False: break

        page += 1

        time.sleep(1)
        print("Searching page:", page)

if __name__ == '__main__':
    run()
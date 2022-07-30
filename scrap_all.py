import json
import os
from pathlib import Path
import time

from AniListPy import anilistpy

def run(media_dir:Path=None, media_type="ANIME", start_page=1) -> None:
    if not media_dir: media_dir = Path("./db/anilist_files/")

    if not isinstance(media_dir, Path):
        media_dir = Path(media_dir)

    if not media_dir.exists():
        media_dir.mkdir(parents=True)

    page = start_page
    al_client = anilistpy.AniList()

    while True:
        response = al_client.query_page(page_num=page, media_type=media_type)
        
        if len(response["data"]["Page"]["media"]) == 0:
            print("Reached last page.\nStopping program.")
            return

        for media in response["data"]["Page"]["media"]:
            filename = media_dir / f"{media['id']}.json"
            if filename.exists():
                print('Skipping "{}"'.format(media["title"]["romaji"]))
                continue

            else:
                if media_type.upper() == "ANIME":
                    media_full_data = al_client.query_anime_id(media["id"])
                else:
                    media_full_data = al_client.query_manga_id(media["id"])
                
                time.sleep(1)
                print("{} \t|\t {}".format(media["id"], media["title"]["romaji"]))

            with filename.open("w+", encoding="utf-8") as outfile:
                json.dump(media_full_data, outfile, indent=4, ensure_ascii=False)

        page += 1

        time.sleep(1)
        print("Searching page:", page)

if __name__ == '__main__':
    run()
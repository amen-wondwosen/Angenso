from argparse import ArgumentParser
import json
from pathlib import Path

from AniListPy.anilistpy import AniList

from utils.logging import get_logger

logger = get_logger(__name__, write_to_file=True)

DEFAULT_PAGE_LIMIT = 3  # max number of pages to search

def main(a:ArgumentParser):
    args = a.parse_args()

    dest = Path(args.destination)

    scrap_media(
        base_path=dest, page_limit=args.page_limit,
        media_type=args.media_type, 
        all_=args.all
    )

def scrap_media(
        base_path: Path,
        page_limit: int = DEFAULT_PAGE_LIMIT,
        media_type: str = "ANIME",
        start_page: int = 1,
        sort_new: bool = True,
        all_: bool = False):

    if not isinstance(base_path, Path):
        base_path = Path(base_path).resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    # normalize media type
    if not media_type.isupper(): media_type = media_type.upper()

    page = start_page
    al_client = AniList()

    # while True:
    while all_ or (page <= page_limit):
        response = al_client.query_page(
            page_num=page,
            media_type=media_type,
            sort_new=sort_new
        )

        current_page = response["data"]["Page"]["pageInfo"]["currentPage"]
        has_next_page = response["data"]["Page"]["pageInfo"]["hasNextPage"]

        for media_metadata in response["data"]["Page"]["media"]:
            AL_id = media_metadata["id"]
            title = media_metadata["title"]["romaji"]

            # Build the filepath using the MAL id as the filename
            dest_path = base_path / f"{AL_id}.json"

            # TODO: Skip old entries only if looking at new entries
            if (all_ != True) and dest_path.exists():
                logger.debug(f'Skipped {AL_id:<6} | <{title}>...')
                continue

            try:
                # Compare the data pulled to the existing copy
                # and skip if there is no difference
                if dest_path.exists():
                    with dest_path.open("r", encoding="utf-8") as infile:
                        local_data = json.load(infile)

                    if media_metadata == local_data: continue

                # Dump metadata to a json file
                with dest_path.open("w+", encoding="utf-8") as outfile:
                    json.dump(media_metadata, outfile, indent=4, ensure_ascii=False)

                if all_ and dest_path.exists():
                    # Updating existing media entry
                    logger.info(f'Updated {AL_id:<6} | <{title}>...')
                else:
                    # Adding new media entry
                    logger.info(f'Scrapped {AL_id:<6} | <{title}>...')
            except KeyboardInterrupt:
                # Manual terminal of program
                logger.error("Program interrupted by keyboard shorcut.")
                raise
            except Exception:
                logger.error("Error encountered when creating file {}.".format(dest_path.name))
                raise

        # Do not continue if next request will be empty
        if has_next_page:
            page += 1
        else:
            break


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        "media_type", choices=["anime", "manga"],
        help="what type of media"
    )
    parser.add_argument(
        "-d", "--destination", type=str, required=True,
        help="where to save files"
    )
    parser.add_argument(
        "-p", "--page_limit", type=int, default=DEFAULT_PAGE_LIMIT,
        required=False, help="number of pages to look at"
    )
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="look at all entries"
    )

    main(parser)
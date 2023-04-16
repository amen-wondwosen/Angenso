
from requests_ratelimiter import Duration, RequestRate, Limiter, LimiterSession

from api import APIHandler
from utils.logging import get_logger

class MyAnimeListAPIHandler(APIHandler):
    def __init__(self) -> None:
        super().__init__()

        self.base_url = "https://api.jikan.moe/v4"
        self._logger = get_logger(__name__, write_to_file=False)

    def get_all(self, start_page, media_type, all_: bool = False, retry_once: bool = True):
        errored_pages = []
        page = start_page
        session = self._create_session()
        url = f"{self.base_url}/{media_type.lower()}"

        # (page <= self.DEFAULT_PAGE_LIMIT) is used over
        # (page <= start_page+self.DEFAULT_PAGE_LIMIT) is because the program
        # assumes that this clause will only be used when looking at the first
        # x number of pages for new entries.
        while all_ or (page <= self.DEFAULT_PAGE_LIMIT):
            params = {
                "page": page,
                "order_by": "mal_id",
                "sort": "desc"
            }

            self._logger.debug(f"Querying page {page}.")
            req = session.get(url, params=params)
            response = req.json()

            current_page = response["pagination"]["current_page"]
            has_next_page = response["pagination"]["has_next_page"]

            for media_metadata in response["data"]:
                # yield id, title, and the complete metadata
                # The id and title should easily accessible.
                yield (
                    media_metadata["mal_id"],
                    media_metadata["title"],
                    media_metadata
                )

            # Do not continue if next request will be empty
            if has_next_page:
                page += 1
            else:
                break

    @staticmethod
    def _create_session() -> LimiterSession:
        mal_rate = RequestRate(1, Duration.SECOND * 4)
        limiter = Limiter(mal_rate)
        return LimiterSession(limiter=limiter)

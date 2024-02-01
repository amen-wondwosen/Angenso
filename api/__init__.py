from abc import ABC, abstractclassmethod


class APIHandler(ABC):
    def __init__(self) -> None:
        self.DEFAULT_PAGE_LIMIT = 3     # Max number of pages to look at

    @abstractclassmethod
    def get_all(self, start_page, media_type, all_: bool = False, retry_once: bool = True):
        pass
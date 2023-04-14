class APICallHandler:
    def __init__(self) -> None:
        self.DEFAULT_PAGE_LIMIT = 5     # Max number of pages to look at

    def get_all(self, start_page, media_type, all_: bool = False, retry_once: bool = True):
        pass
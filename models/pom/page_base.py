from abc import ABCMeta, abstractmethod

from helpers.helpers_container import HelpersContainer


class PageBase(object, metaclass=ABCMeta):
    def __init__(self, helpers: HelpersContainer, page_title: str, page_path: str):
        self.helpers = helpers
        self.playwright_page = helpers.playwright.page
        self.playwright_page.wait_for_load_state(state="networkidle")
        self.page_title = page_title
        self.page_path = page_path
        self._init_locators()
        self._init_components()

    @abstractmethod
    def _init_locators(self):
        pass

    @abstractmethod
    def _init_components(self):
        pass

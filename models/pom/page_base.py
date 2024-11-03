from abc import ABCMeta, abstractmethod

from helpers.helpers_container import HelpersContainer


class PageBase(object, metaclass=ABCMeta):
    def __init__(self, helpers: HelpersContainer, page_title: str):
        self.helpers = helpers
        self.playwright_page = helpers.playwright.page
        self.page_title = page_title
        self._init_locators()

    @abstractmethod
    def _init_locators(self):
        pass
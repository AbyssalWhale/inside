from abc import ABCMeta, abstractmethod

from helpers.helpers_container import HelpersContainer


class ComponentsBase(object, metaclass=ABCMeta):
    def __init__(self, helpers: HelpersContainer):
        self.helpers = helpers
        self.playwright_page = helpers.playwright.page
        self._init_locators()

    @abstractmethod
    def _init_locators(self):
        pass
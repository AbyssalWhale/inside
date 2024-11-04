from abc import ABCMeta, abstractmethod

from helpers.helpers_container import HelpersContainer
from playwright.sync_api import Locator
from models.pom.components.cookies_window import CookiesWindow
from models.pom.components.navigation_component import NavigationComponent


class PageBase(object, metaclass=ABCMeta):
    def __init__(self, helpers: HelpersContainer, page_title: str, page_path: str):
        self.helpers = helpers
        self.playwright_page = helpers.playwright.page
        self.playwright_page.wait_for_load_state(state="networkidle")
        self.page_title = page_title
        self.page_path = page_path
        self._init_locators()
        self._init_components()
        self.__init_common_components()

    @abstractmethod
    def _init_locators(self):
        pass

    @abstractmethod
    def _init_components(self):
        pass

    def __init_common_components(self):
        self._navigation = NavigationComponent(helpers=self.helpers)
        self._cookies_window = CookiesWindow(helpers=self.helpers)

    def _click_on_element_and_switch_tab(self, locator: Locator):
        locator.wait_for(state="visible")
        with self.playwright_page.expect_popup() as new_tab:
            locator.click()
        self.helpers.playwright.page = new_tab.value
        self.playwright_page = new_tab.value

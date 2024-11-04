from helpers.helpers_container import HelpersContainer
from models.pom.components_base import ComponentsBase


class CookiesWindow(ComponentsBase):
    def __init__(self, helpers: HelpersContainer):
        super().__init__(helpers=helpers)

    def _init_locators(self):
        self.__button_accept_all = self.playwright_page.locator("a[id='wt-cli-accept-all-btn']")

    def click_accept_all_cookies(self):
        if self.__button_accept_all.is_visible():
            self.__button_accept_all.click()
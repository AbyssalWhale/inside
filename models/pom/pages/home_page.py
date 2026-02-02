from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helpers_container import HelpersContainer
from models.pom.components.navigation_component import NavigationComponent
from models.pom.page_base import PageBase
from models.pom.pages.careers.careers_page import CareersPage


class HomePage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider One"):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="")
        self.playwright_page.goto(
            url=helpers.test_run_config.get_property_value(property_name=EnumsTestRunConfigProperties.URL))

    def _init_locators(self):
        self.__header = self.playwright_page.locator("header")
        self.__footer = self.playwright_page.locator("footer")

    def _init_components(self):
        pass

    def are_main_blocks_loaded(self):
        header_visible = self.__header.first.is_visible()
        footer_visible = self.__footer.first.is_visible()
        return header_visible and footer_visible

    def navigate_to_careers(self):
        self._navigation.navigate_to_careers()
        return CareersPage(helpers=self.helpers)

    def accept_cookies(self):
        self._cookies_window.click_accept_all_cookies()

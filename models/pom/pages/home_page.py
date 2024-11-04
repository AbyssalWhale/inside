from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helpers_container import HelpersContainer
from models.pom.components.navigation_component import NavigationComponent
from models.pom.page_base import PageBase
from models.pom.pages.careers.careers_page import CareersPage


class HomePage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="#1 Leader in Individualized, Cross-Channel CX — Insider"):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="")
        self.playwright_page.goto(
            url=helpers.test_run_config.get_property_value(property_name=EnumsTestRunConfigProperties.URL))

    def _init_locators(self):
        pass

    def _init_components(self):
        self.__navigation = NavigationComponent(helpers=self.helpers)

    def navigate_to_careers(self):
        self.__navigation.navigate_to_careers()
        return CareersPage(helpers=self.helpers)

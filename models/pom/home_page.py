from abc import ABC

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase


class HomePage(PageBase, ABC):
    def __init__(self, helpers: HelpersContainer, page_title="#1 Leader in Individualized, Cross-Channel CX — Insider"):
        super().__init__(
            helpers=helpers,
            page_title=page_title)
        self.playwright_page.goto(
            url=helpers.test_run_config.get_property_value(property_name=EnumsTestRunConfigProperties.URL))

    def _init_locators(self):
        pass

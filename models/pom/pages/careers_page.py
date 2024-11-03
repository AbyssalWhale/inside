from email.policy import strict

from helpers.helpers_container import HelpersContainer
from models.pom.components.navigation_component import NavigationComponent
from models.pom.page_base import PageBase

class CareersPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="#1 Leader in Individualized, Cross-Channel CX — Insider"):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers")

    def _init_locators(self):
        self.__job_items = self.playwright_page.locator("div.job-item")

    def _init_components(self):
        self.__navigation = NavigationComponent(helpers=self.helpers)

    def is_find_your_calling_block_closed(self):
        return self.__job_items.count() == 3
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
        pass

    def _init_components(self):
        self.__navigation = NavigationComponent(helpers=self.helpers)
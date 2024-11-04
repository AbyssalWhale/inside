from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase


class OpeningJobsPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider Open Positions | Insider "):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers/open-positions")

    def _init_locators(self):
        pass

    def _init_components(self):
        pass
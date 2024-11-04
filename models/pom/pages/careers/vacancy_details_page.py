from enums.playw.objects_states import ElementStates
from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase


class VacancyDetailsPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title: str):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="useinsider/")

    def get_title(self):
        self.__label_title.wait_for(state=ElementStates.VISIBLE.value)
        return self.__label_title.text_content()

    def get_vacancy_location(self):
        self.__label_location.wait_for(state=ElementStates.VISIBLE.value)
        return self.__label_location.text_content()

    def _init_locators(self):
        self.__label_title = self.playwright_page.locator("//div[@class='posting-headline']/h2")
        self.__label_location = self.playwright_page.locator("//div[contains(@class, 'location')]")

    def _init_components(self):
        pass
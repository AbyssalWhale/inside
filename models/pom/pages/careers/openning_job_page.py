from enums.playw.objects_states import ElementStates
from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase
from models.pom.pages.careers.vacancy_details_page import VacancyDetailsPage


class OpeningJobsPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider Open Positions | Insider "):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers/open-positions")

    def is_department_selected(self, department: str):
        return self.playwright_page.locator(f"//span[@title='{department}']") is not None

    def set_location(self, location: str, department_to_wait_for: str):
        self.__drop_down_open_location.click()
        self.playwright_page.locator(f"//li[text()='{location}']").click()
        locator_to_wait = self.playwright_page.locator(f"//span[contains(@class, 'position-department') and text()='{department_to_wait_for}']")
        locator_to_wait.wait_for(
            state=ElementStates.VISIBLE.value,
            timeout=10000)

    def get_jobs_titles(self):
        self.__label_jobs_titles.wait_for(
            state=ElementStates.VISIBLE.value,
            timeout=10000)
        return self.__label_jobs_titles.all_inner_texts()

    def get_jobs_departments(self):
        return self.__label_jobs_departments.all_inner_texts()

    def get_jobs_locations(self):
        return self.__label_jobs_locations.all_inner_texts()

    def click_view_role(self, vacancy_name: str):
        self.playwright_page.get_by_text(vacancy_name).hover()
        self._click_on_element_and_switch_tab(locator=self.__button_view_role)
        return VacancyDetailsPage(
            helpers=self.helpers,
            page_title=f"Insider. - {vacancy_name}")

    def _init_locators(self):
        self.__drop_down_open_location = self.playwright_page.locator("//span[contains(@aria-labelledby, 'location')]")
        self.__label_jobs_titles = self.playwright_page.locator("//p[contains(@class, 'position-title')]")
        self.__label_jobs_departments = self.playwright_page.locator("//span[contains(@class, 'position-department')]")
        self.__label_jobs_locations = self.playwright_page.locator("//div[contains(@class, 'position-location')]")
        self.__section_pagination = self.playwright_page.locator("section[id='pagination']")
        self.__button_view_role = self.playwright_page.get_by_text("View Role")

    def _init_components(self):
        pass
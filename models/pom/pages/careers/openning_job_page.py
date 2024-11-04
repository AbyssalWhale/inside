from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase


class OpeningJobsPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider Open Positions | Insider "):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers/open-positions")

    def is_department_selected(self, department: str):
        return self.playwright_page.locator(f"//span[@title='{department}']") is not None

    def set_location(self, location: str):
        self.__drop_down_open_location.click()
        self.playwright_page.locator(f"//li[text()='{location}']").click()

    def get_jobs_titles(self):
        self.__label_jobs_titles.wait_for(state="visible")
        return self.__label_jobs_titles.all_inner_texts()

    def get_jobs_departments(self):
        return self.__label_jobs_departments.all_inner_texts()

    def get_jobs_locations(self):
        return self.__label_jobs_locations.all_inner_texts()

    def _init_locators(self):
        self.__drop_down_open_location = self.playwright_page.locator("//span[contains(@aria-labelledby, 'location')]")
        self.__label_jobs_titles = self.playwright_page.locator("//p[contains(@class, 'position-title')]")
        self.__label_jobs_departments = self.playwright_page.locator("//span[contains(@class, 'position-department')]")
        self.__label_jobs_locations = self.playwright_page.locator("//div[contains(@class, 'position-location')]")

    def _init_components(self):
        pass
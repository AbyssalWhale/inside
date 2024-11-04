from os import path

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase
from models.pom.pages.careers.openning_job_page import OpeningJobsPage


class QACareers(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider quality assurance job opportunities"):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers/quality-assurance/")

    def goto_by_url(self):
        url = path.join(
            self.helpers.test_run_config.get_property_value(property_name=EnumsTestRunConfigProperties.URL),
            self.page_path)
        self.playwright_page.goto(url)

    def click_button_see_all_qa_jobs(self):
        self.__button_see_all_qa_jobs.click()
        return OpeningJobsPage(helpers=self.helpers)

    def _init_locators(self):
        self.__button_see_all_qa_jobs = self.playwright_page.locator("//a[text()='See all QA jobs']")

    def _init_components(self):
        pass
from enums.playw.objects_states import ElementStates
from helpers.helpers_container import HelpersContainer
from models.pom.page_base import PageBase
from models.pom.pages.careers.vacancy_details_page import VacancyDetailsPage


class OpeningJobsPage(PageBase):
    def __init__(self, helpers: HelpersContainer, page_title="Insider One"):
        super().__init__(
            helpers=helpers,
            page_title=page_title,
            page_path="careers/open-positions")

    def wait_for_filters_loaded(self):
        self.__select_location.wait_for(
            state=ElementStates.VISIBLE.value,
            timeout=10000)
        self.playwright_page.wait_for_function(
            "document.querySelectorAll('#filter-by-location option').length > 1",
            timeout=15000)

    def is_department_selected(self, department: str):
        selected = self.__select_department.input_value()
        return selected == department

    def set_location(self, location: str):
        self.__select_location.select_option(label=location)
        self.__select_location.dispatch_event("change")
        self.playwright_page.wait_for_timeout(2000)

    def set_department(self, department: str):
        self.__select_department.select_option(label=department)
        self.__select_department.dispatch_event("change")
        self.playwright_page.wait_for_timeout(2000)

    def _get_filtered_item_locator(self):
        loc_value = self.__select_location.input_value()
        dept_value = self.__select_department.input_value()
        selector = "div.position-list-item"
        if loc_value and loc_value != "All":
            data_loc = loc_value.replace(" ", "").replace(",", "").lower()
            selector += f'[data-location="{data_loc}"]'
        if dept_value and dept_value != "All":
            data_team = dept_value.replace(" ", "").lower()
            selector += f'[data-team="{data_team}"]'
        return self.playwright_page.locator(selector)

    def get_jobs_titles(self):
        items = self._get_filtered_item_locator()
        items.first.wait_for(state=ElementStates.VISIBLE.value, timeout=10000)
        return items.locator("p.position-title").all_inner_texts()

    def get_jobs_departments(self):
        items = self._get_filtered_item_locator()
        return items.locator("span.position-department").all_inner_texts()

    def get_jobs_locations(self):
        items = self._get_filtered_item_locator()
        return items.locator("div.position-location").all_inner_texts()

    def click_view_role(self):
        items = self._get_filtered_item_locator()
        items.first.locator("p.position-title").hover()
        view_btn = items.first.locator("a.btn")
        view_btn.wait_for(state=ElementStates.VISIBLE.value, timeout=10000)
        self._click_on_element_and_switch_tab(locator=view_btn)
        return VacancyDetailsPage(helpers=self.helpers)

    def _init_locators(self):
        self.__select_location = self.playwright_page.locator("#filter-by-location")
        self.__select_department = self.playwright_page.locator("#filter-by-department")

    def _init_components(self):
        pass

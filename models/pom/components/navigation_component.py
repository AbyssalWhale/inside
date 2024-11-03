from helpers.helpers_container import HelpersContainer
from models.pom.components_base import ComponentsBase


class NavigationComponent(ComponentsBase):
    def __init__(self, helpers: HelpersContainer):
        super().__init__(helpers=helpers)

    def _init_locators(self):
        self._main_menu_company = self.playwright_page.locator("//a[contains(text(), 'Company')]")
        self._submenu_careers = self.playwright_page.locator("//a[contains(text(), 'Careers')]")

    def navigate_to_careers(self):
        self._main_menu_company.click()
        self._submenu_careers.click()
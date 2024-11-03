import pytest
from playwright.sync_api import Playwright

from helpers.helpers_container import HelpersContainer
from models.pom.pages.home_page import HomePage


@pytest.fixture(scope="session")
def set_up(playwright: Playwright):
    helpers = HelpersContainer(playwright=playwright)
    home_page = HomePage(helpers=helpers)

    yield home_page, helpers

    helpers.playwright.context.close()

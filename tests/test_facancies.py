import re

import pytest
from playwright.sync_api import expect
from conftest import set_up


@pytest.fixture(scope="function")
def suit_set_up(set_up):
    home_page, helpers = set_up
    expect(home_page.playwright_page).to_have_title(re.compile(home_page.page_title))

    yield home_page, helpers


def test_can_observe_vacancy(suit_set_up):
    # Expect a title "to contain" a substring.
    home_page, helpers = suit_set_up

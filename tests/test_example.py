import re

from playwright.sync_api import expect


def test_can_observe_vacancy(set_up):
    # Expect a title "to contain" a substring.
    home_page, helpers = set_up

    expect(home_page.playwright_page).to_have_title(re.compile(home_page.page_title))

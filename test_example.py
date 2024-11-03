import re

import pytest
from playwright.sync_api import expect, Playwright


@pytest.fixture(scope="session")
def set_up(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://useinsider.com/")

    yield page

    page.close()
    context.close()
    browser.close()


def test_can_observe_vacancy(set_up):
    # Expect a title "to contain" a substring.
    page = set_up
    expect(page).to_have_title(re.compile("#1 Leader in Individualized, Cross-Channel CX — Insider"))

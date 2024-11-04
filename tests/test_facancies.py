import re

import pytest
from playwright.sync_api import expect
from conftest import set_up


@pytest.fixture(scope="function")
def suit_set_up(set_up):
    home_page, helpers = set_up
    expect(home_page.playwright_page).to_have_title(re.compile(home_page.page_title))
    careers_page = home_page.navigate_to_careers()
    assert careers_page.page_path in careers_page.playwright_page.url
    # Teams and Life at Insider blocks - I could not find these blocks.
    # Check 'Find your calling'
    assert careers_page.is_find_your_calling_block_closed() is True

    yield careers_page, helpers


@pytest.mark.regression
def test_qa_vacancy_can_observe(suit_set_up):
    # Expect a title "to contain" a substring.
    careers_page, helpers = suit_set_up
    qa_careers_page = careers_page.goto_qa_careers_via_url()
    expect(qa_careers_page.playwright_page).to_have_title(re.compile(qa_careers_page.page_title))
    opening_positions_page = qa_careers_page.click_button_see_all_qa_jobs()
    expect(opening_positions_page.playwright_page).to_have_title(re.compile(opening_positions_page.page_title))
    print("done!")

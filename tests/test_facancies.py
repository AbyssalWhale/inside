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
@pytest.mark.parametrize("location, department, vacancy", [("Istanbul, Turkey", "Quality Assurance", "Senior Software Quality Assurance Engineer")])
def test_qa_vacancy_can_observe(suit_set_up, location, department, vacancy):
    careers_page, helpers = suit_set_up

    # go to open positions
    qa_careers_page = careers_page.goto_qa_careers_via_url()
    expect(qa_careers_page.playwright_page).to_have_title(re.compile(qa_careers_page.page_title))
    opening_positions_page = qa_careers_page.click_button_see_all_qa_jobs()
    expect(opening_positions_page.playwright_page).to_have_title(re.compile(opening_positions_page.page_title))

    # go to vacancy details
    opening_positions_page.set_location(location=location, department_to_wait_for=department)
    assert opening_positions_page.is_department_selected(department) is True
    assert all(department.lower() in title.lower() for title in opening_positions_page.get_jobs_titles())
    assert all(department.lower() in title.lower() for title in opening_positions_page.get_jobs_departments())
    assert all(location.lower() in title.lower() for title in opening_positions_page.get_jobs_locations())
    vacancy_details_page = opening_positions_page.click_view_role(vacancy_name=vacancy)

    # assert vacancy details
    expect(vacancy_details_page.playwright_page).to_have_title(re.compile(vacancy_details_page.page_title))
    assert vacancy_details_page.get_title() == vacancy
    assert vacancy_details_page.get_vacancy_location() == location

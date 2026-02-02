import re

import pytest
from playwright.sync_api import expect
from models.pom.pages.careers.qa_careers_page import QACareers


@pytest.mark.regression
def test_qa_vacancy_can_observed(set_up):
    home_page, helpers = set_up

    location = "Istanbul, Turkiye"
    department = "Quality Assurance"

    # Step 3.1: Verify home page is opened and main blocks are loaded
    expect(home_page.playwright_page).to_have_title(re.compile(home_page.page_title))
    assert home_page.are_main_blocks_loaded(), "Main blocks (navbar, footer) are not loaded on the home page"

    # Step 3.2: Go to QA careers page, click "See all QA jobs", filter by location and department
    qa_careers_page = QACareers(helpers=helpers)
    qa_careers_page.goto_by_url()
    opening_positions_page = qa_careers_page.click_button_see_all_qa_jobs()
    opening_positions_page.wait_for_filters_loaded()
    opening_positions_page.set_department(department=department)
    opening_positions_page.set_location(location=location)
    assert opening_positions_page.is_department_selected(department) is True

    jobs_titles = opening_positions_page.get_jobs_titles()
    assert len(jobs_titles) > 0, "No jobs found after filtering"

    # Step 3.3: Check that all jobs contain expected values
    jobs_departments = opening_positions_page.get_jobs_departments()
    jobs_locations = opening_positions_page.get_jobs_locations()

    assert all(department.lower() in title.lower() for title in jobs_titles), \
        f"Not all job positions contain '{department}'"
    assert all(department.lower() in dept.lower() for dept in jobs_departments), \
        f"Not all job departments contain '{department}'"
    assert all(location.lower() in loc.lower() for loc in jobs_locations), \
        f"Not all job locations contain '{location}'"

    # Step 3.4: Click "View Role" and check redirect to Lever Application form page
    vacancy_details_page = opening_positions_page.click_view_role()
    assert vacancy_details_page.is_lever_application_page(), \
        f"Expected Lever application page (lever.co), got: {vacancy_details_page.playwright_page.url}"

    vacancy_title = vacancy_details_page.get_title()
    assert department.lower() in vacancy_title.lower(), \
        f"Vacancy title '{vacancy_title}' does not contain '{department}'"

    vacancy_location = vacancy_details_page.get_vacancy_location()
    assert location.lower() in vacancy_location.lower(), \
        f"Vacancy location '{vacancy_location}' does not contain '{location}'"

    assert vacancy_details_page.is_apply_button_visible(), \
        "Apply for this job button is not visible"

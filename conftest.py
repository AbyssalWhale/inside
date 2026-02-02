import os

import pytest
from playwright.sync_api import sync_playwright

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helpers_container import HelpersContainer
from helpers.helper_test_run_config import HelperTestRunConfig
from helpers.helper_system import HelperSystem
from models.pom.pages.home_page import HomePage


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default=None,
        help="Browser to run tests in: chromium or firefox",
    )


@pytest.fixture(params=["chromium", "firefox"])
def browser_name(request):
    cli_browser = request.config.getoption("--browser-name")
    if cli_browser:
        if request.param != cli_browser:
            pytest.skip(f"Skipping {request.param}, CLI selected {cli_browser}")
        return cli_browser
    return request.param


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def set_up(browser_name, request):
    pw = sync_playwright().start()
    helpers = HelpersContainer(playwright=pw, browser_name=browser_name)
    helpers.playwright.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    home_page = HomePage(helpers=helpers)
    home_page.accept_cookies()

    yield home_page, helpers

    # Save trace only on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            results_dir = helpers.test_run_config.get_property_value(
                property_name=EnumsTestRunConfigProperties.TESTS_RESULTS_DIR)
            os.makedirs(results_dir, exist_ok=True)
            trace_name = f"{request.node.name}_{browser_name}.zip"
            trace_path = os.path.join(results_dir, trace_name)
            helpers.playwright.context.tracing.stop(path=trace_path)
        except Exception:
            helpers.playwright.context.tracing.stop()
    else:
        helpers.playwright.context.tracing.stop()

    helpers.playwright.context.close()
    helpers.playwright.browser.close()
    pw.stop()

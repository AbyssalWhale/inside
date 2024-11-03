from playwright.sync_api import Playwright
import os

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helper_test_run_config import HelperTestRunConfig


class HelperPlaywright:
    def __init__(self, playwright: Playwright, test_run_config: HelperTestRunConfig):
        self.playwright = playwright
        self.browser = self.playwright.chromium.launch(
            headless=test_run_config.get_property_value(
                property_name=EnumsTestRunConfigProperties.HEADLESS),
            args=["--start-maximized"]
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(10000.00)

from playwright.sync_api import Playwright

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helper_test_run_config import HelperTestRunConfig


class HelperPlaywright:
    def __init__(self, playwright: Playwright, test_run_config: HelperTestRunConfig, browser_name: str = "chromium"):
        self.playwright = playwright

        browser_type = getattr(self.playwright, browser_name, self.playwright.chromium)

        launch_args = []
        if browser_name == "chromium":
            launch_args.append("--start-maximized")

        self.browser = browser_type.launch(
            headless=test_run_config.get_property_value(property_name=EnumsTestRunConfigProperties.HEADLESS),
            args=launch_args
        )
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080})
        self.page = self.context.new_page()
        self.page.set_default_timeout(10000.00)

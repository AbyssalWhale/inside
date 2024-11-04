from playwright.sync_api import Playwright

from helpers.helper_playwright import HelperPlaywright
from helpers.helper_system import HelperSystem
from helpers.helper_test_run_config import HelperTestRunConfig


class HelpersContainer:
    def __init__(self, playwright: Playwright):
        self.system = HelperSystem()
        self.test_run_config = HelperTestRunConfig(system_helper=self.system)
        self.playwright = HelperPlaywright(
            playwright=playwright,
            test_run_config=self.test_run_config)
from enum import Enum


class EnumsTestRunConfigProperties(Enum):
    __test__ = False
    URL = "url"
    HEADLESS = "headless"
    TESTS_RESULTS_DIR = "tests-result-dir"

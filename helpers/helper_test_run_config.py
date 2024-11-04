import json
import os

from enums.tests.enums_test_run_config_properties import EnumsTestRunConfigProperties
from helpers.helper_system import HelperSystem


class HelperTestRunConfig:
    def __init__(self, system_helper: HelperSystem):
        self._system_helper = system_helper
        self._config = self._get_config()
        self._set_test_results_dir()

    def get_property_value(self, property_name: EnumsTestRunConfigProperties):
        return self._config[str(property_name.value)]

    def _set_test_results_dir(self):
        tests_result_dir_path = os.path.join(
            self._system_helper.get_project_dir(),
            self.get_property_value(property_name=EnumsTestRunConfigProperties.TESTS_RESULTS_DIR))
        self._config[EnumsTestRunConfigProperties.TESTS_RESULTS_DIR.value] = tests_result_dir_path
        os.makedirs(tests_result_dir_path, exist_ok=True)

    def _get_config(self):
        file_name = "test-run-config.json"
        full_file_path = os.path.join(
            self._system_helper.get_project_dir(),
            file_name)
        if os.path.exists(full_file_path):
            with open(full_file_path) as f:
                result = json.load(f)
                return result
        else:
            raise Exception(f"could not find test run config: {file_name}. Path: {full_file_path}")
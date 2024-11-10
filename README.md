# Enviroment Requrements
- [Python](https://www.python.org/downloads/)
- [PIP](https://pypi.org/project/pip/)
- [Pycharm](https://www.jetbrains.com/pycharm/)
- packages from ```requirements.txt```
- [playwright](https://playwright.dev/python/docs/intro)

# High-Level Structure
```
├── .github - github action wrokflows
├── enums - project enums grouped by category: playwright, sut (system under test), tests_enum. 
├── helpers - helpers that are used interact with browser, system and test-run-config.json
├── models - project models grouped by category: api, poms (Page Object Models) etc
├── tests - all project tests
├── .gitignore - list of ignored items by git
├── conftest.py - fixtures
├── pytest.ini - pytest configuration file
├── README.md - readme file 
├── requirements.txt - required packages 
└── test-run-config.json - test run config file that is used during test execution. Contains: URL, credentials, keys etc.
```

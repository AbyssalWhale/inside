# Insider One QA Test Automation

Playwright-based test automation project for [insiderone.com](https://insiderone.com/). Tests run in both Chromium and Firefox browsers with automatic Playwright trace capture on failure.

## Project Structure

```
├── .github/            - GitHub Actions workflows
├── enums/              - Project enums (element states, config properties)
├── helpers/            - Browser, system, and config helpers
├── models/pom/         - Page Object Models and reusable components
├── tests/              - Test files
├── conftest.py         - Pytest fixtures (browser setup, trace-on-failure)
├── pytest.ini          - Pytest configuration
├── requirements.txt    - Python dependencies
└── test-run-config.json - Runtime config (URL, headless mode, browser)
```

## Prerequisites

### 1. Install Python 3.10+

**macOS** (using Homebrew):
```bash
brew install python
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Windows**:

Download and install from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during installation.

Verify installation:
```bash
python3 --version
pip3 --version
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd inside
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

```bash
playwright install chromium firefox
```

## Configuration

Edit `test-run-config.json` to change runtime settings:

```json
{
  "url": "https://insiderone.com/",
  "headless": true,
  "tests-result-dir": "./tests-results/"
}
```

- `headless` - set to `false` to see the browser window during test execution
- `tests-result-dir` - directory where trace files are saved on failure

## Running Tests

Make sure the virtual environment is activated before running tests.

**Run in both Chromium and Firefox:**
```bash
pytest -m regression
```

**Run in Chromium only:**
```bash
pytest -m regression --browser-name chromium
```

**Run in Firefox only:**
```bash
pytest -m regression --browser-name firefox
```

**Run a specific test file:**
```bash
pytest tests/test_vacancies.py -m regression --browser-name chromium
```

## Test Output

- Console output is verbose by default (`-v` in `pytest.ini`)
- Browser name is shown in each test ID, e.g. `test_qa_vacancy_can_observed[chromium]`
- On failure, a Playwright trace (`.zip`) is saved to `tests-results/`

**Viewing a trace:**
```bash
playwright show-trace tests-results/<trace-file>.zip
```
This opens the Trace Viewer with a full timeline of actions, DOM snapshots, network requests, and console logs.

## Test Case: `test_qa_vacancy_can_observed`

1. Visit https://insiderone.com/ and verify the home page loads with main blocks (navbar, footer)
2. Navigate to QA careers page, click "See all QA jobs", filter by Istanbul, Turkiye and Quality Assurance, verify jobs are listed
3. Assert all filtered jobs have correct Position, Department, and Location values
4. Click "View Role" and verify redirect to Lever application form page

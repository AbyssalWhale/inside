# Insider One QA Test Automation

This project contains two types of tests:

- **UI Tests** — Playwright-based browser tests for [insiderone.com](https://insiderone.com/) (Chromium & Firefox)
- **Load Tests** — Locust-based HTTP load tests for search functionality on [n11.com](https://www.n11.com/)

---

## UI Tests (Playwright)

Browser-driven test automation with automatic trace capture on failure.

### Project Structure

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

### Prerequisites

#### 1. Install Python 3.10+

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

#### 2. Clone the Repository

```bash
git clone <repository-url>
cd inside
```

#### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Install Playwright Browsers

```bash
playwright install chromium firefox
```

### Configuration

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

### Running UI Tests

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

### Test Output

- Console output is verbose by default (`-v` in `pytest.ini`)
- Browser name is shown in each test ID, e.g. `test_qa_vacancy_can_observed[chromium]`
- On failure, a Playwright trace (`.zip`) is saved to `tests-results/`

**Viewing a trace:**
```bash
playwright show-trace tests-results/<trace-file>.zip
```
This opens the Trace Viewer with a full timeline of actions, DOM snapshots, network requests, and console logs.

### Test Case: `test_qa_vacancy_can_observed`

1. Visit https://insiderone.com/ and verify the home page loads with main blocks (navbar, footer)
2. Navigate to QA careers page, click "See all QA jobs", filter by Istanbul, Turkiye and Quality Assurance, verify jobs are listed
3. Assert all filtered jobs have correct Position, Department, and Location values
4. Click "View Role" and verify redirect to Lever application form page

---

## API Tests (Petstore)

Automated CRUD tests for the [Petstore Swagger API](https://petstore.swagger.io/v2) using `requests` + `pytest`.

### Directory Structure

```
api_tests/
├── __init__.py        - Package marker
├── config.py          - Base URL, headers, status codes
├── pet_builder.py     - Builder pattern for pet payloads
├── conftest.py        - Fixtures (api_client, created_pet, pet_data)
├── test_pet_create.py - Create (POST) tests
├── test_pet_read.py   - Read (GET) tests
├── test_pet_update.py - Update (PUT/POST) tests
└── test_pet_delete.py - Delete (DELETE) tests
```

### Running API Tests

```bash
# Run all API tests
pytest -m api

# Run a specific test file
pytest api_tests/test_pet_create.py

# Run a specific test
pytest api_tests/test_pet_read.py::TestReadPetPositive::test_get_pet_by_id
```

### Endpoints Tested

| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| POST   | `/pet`                 | Create a new pet        |
| GET    | `/pet/{petId}`         | Get pet by ID           |
| GET    | `/pet/findByStatus`    | Find pets by status     |
| PUT    | `/pet`                 | Update an existing pet  |
| POST   | `/pet/{petId}`         | Update pet with form    |
| DELETE | `/pet/{petId}`         | Delete a pet            |

### Adding New Tests

1. Add new test files in `api_tests/` following the `test_pet_*.py` naming convention
2. Use `PetBuilder` from `pet_builder.py` to construct request payloads
3. Use the `api_client` fixture for HTTP requests and `created_pet` for tests that need pre-existing data
4. Mark test classes or functions with `@pytest.mark.api`

---

## Load Tests (Locust)

HTTP-based load tests using [Locust](https://locust.io/) to test search functionality on https://www.n11.com/.

### Directory Structure

```
load_tests/
├── __init__.py      - Package marker
├── config.py        - Search terms, headers, and URL constants
├── locustfile.py    - Locust test definition (N11SearchUser)
└── locust.conf      - Default run configuration
```

### Setup

```bash
pip install -r requirements.txt
locust --version
```

### Running Load Tests

**Headless mode (default config — 1 user, 60s):**
```bash
locust --config load_tests/locust.conf
```

**Web UI mode (open http://localhost:8089 in Chrome to configure and start):**
```bash
locust -f load_tests/locustfile.py --host https://www.n11.com
```

**Custom parameters:**
```bash
locust -f load_tests/locustfile.py --host https://www.n11.com \
  --users 1 --spawn-rate 1 --run-time 20s --headless
```

**Export results to CSV:**
```bash
locust --config load_tests/locust.conf --csv load_test_results/run1
```

### Parameters

| Parameter       | Description                              | Example          |
|-----------------|------------------------------------------|------------------|
| `--users`       | Number of concurrent simulated users     | `10`             |
| `--spawn-rate`  | Users spawned per second                 | `2`              |
| `--run-time`    | Total test duration (headless mode)      | `120s`           |
| `--host`        | Target base URL                          | `https://www.n11.com` |
| `--headless`    | Run without the web UI                   | (flag)           |
| `--csv`         | Prefix for CSV result files              | `results/run1`   |

### Metrics Interpretation

| Metric    | Description                                          |
|-----------|------------------------------------------------------|
| Avg       | Average response time in milliseconds                |
| Min       | Fastest response time observed                       |
| Max       | Slowest response time observed                       |
| Median    | 50th percentile response time                        |
| 95%ile    | 95th percentile — 95% of requests were faster        |
| Req/s     | Requests per second throughput                       |
| Failures  | Count of failed requests (non-200 or explicit fails) |

### Configuring Search Terms

Edit `load_tests/config.py` to add, remove, or change search terms. Terms are organized by category (`electronics`, `clothing`, `home_appliances`) and automatically flattened into `ALL_SEARCH_TERMS` for random selection during tests.

---

## Bosun Part

### CI/CD Pipeline

The GitHub Actions pipeline is defined in `.github/workflows/main.yml` and is triggered on **push** and **pull request** events to the `insider-second-task` branch.

The pipeline runs three independent jobs in parallel — no job depends on another, so they execute concurrently for faster feedback.

### Pipeline Jobs

| Job | Description | Command | Artifacts |
|-----|-------------|---------|-----------|
| **UI Tests** | Playwright browser tests (Chromium & Firefox) | `pytest -m regression --junitxml=tests-results/ui-test-results.xml` | `ui-test-results` — JUnit XML + Playwright traces |
| **API Tests** | Petstore API CRUD tests | `pytest -m api --junitxml=tests-results/api-test-results.xml` | `api-test-results` — JUnit XML |
| **Load Tests** | Locust load tests against n11.com | `locust --config load_tests/locust.conf --csv ... --html ...` | `load-test-results` — CSV stats + HTML report |

### Pipeline Workflow

```
push / PR to insider-second-task
            │
    ┌───────┼───────┐
    │       │       │
    ▼       ▼       ▼
 UI Tests  API    Load
 (pytest)  Tests  Tests
           (pytest)(locust)
    │       │       │
    ▼       ▼       ▼
 Upload   Upload  Upload
 Artifacts Artifacts Artifacts
    │       │
    ▼       ▼
 Publish  Publish
 JUnit    JUnit
 Results  Results
```

### Viewing Results

- **Artifacts**: After a workflow run completes, download artifacts from the **Actions** tab in GitHub. Each job uploads its results as a separate artifact.
- **PR Check Results**: UI Tests and API Tests publish JUnit results directly to the PR using `EnricoMi/publish-unit-test-result-action`. Look for the **UI Test Results** and **API Test Results** checks on the pull request.
- **Load Test Report**: Download the `load-test-results` artifact to view the Locust HTML report and CSV statistics locally.

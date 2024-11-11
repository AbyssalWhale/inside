import requests
import time
import os

# Define the test cases with the specific marker for regression tests
test_cases = [{"test_name": "test_login", "marker": "regression"}, {"test_name": "test_signup", "marker": "regression"}]

# Test Runner Service URL from environment variable or can read from config
runner_url = os.getenv("TEST_RUNNER_URL", "http://test-runner-service:8080/run-test")

def send_test_cases():
    for case in test_cases:
        try:
            # Send each test case with the "regression" marker to the Test Runner Pod
            response = requests.post(runner_url, json=case)
            print(f"Sent test case {case}, response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send test case {case}: {e}")
        time.sleep(2)  # Delay to simulate sequential execution

if __name__ == "__main__":
    print("Starting Test Case Controller...")
    send_test_cases()
    print("All test cases sent.")
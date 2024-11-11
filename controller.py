import os
import time
import subprocess
import requests

test_cases = [{"test_name": "test_login", "marker": "regression"}, {"test_name": "test_signup", "marker": "regression"}]

runner_url = os.getenv("TEST_RUNNER_URL", "http://test-runner-service:8080/run-test")

MAX_RETRIES = 5
RETRY_DELAY = 5

node_count = int(os.getenv("NODE_COUNT", 5))


def is_test_runner_ready():
    try:
        dummy_data = {"test_name": "dummy_test", "marker": "regression"}
        response = requests.post(runner_url, json=dummy_data)

        if response.status_code == 200:
            print("Test Runner is ready.")
            return True
        else:
            print(f"Test Runner returned status code {response.status_code}, not ready.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking Test Runner status: {e}")
        return False


def send_test_cases():
    for case in test_cases:
        retry_count = 0
        while retry_count < MAX_RETRIES:
            try:
                print(f"Sending test case {case['test_name']} to {runner_url}")

                response = requests.post(runner_url, json=case)

                print(f"Response from Test Runner: {response.status_code} - {response.text}")

                if response.status_code == 200:
                    print(f"Successfully sent test case {case['test_name']}, response: {response.status_code}")
                    # Exit retry loop if successful
                    break
                else:
                    print(f"Failed to run test case {case['test_name']}, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send test case {case['test_name']}: {e}")

            retry_count += 1
            if retry_count < MAX_RETRIES:
                print(f"Retrying ({retry_count}/{MAX_RETRIES}) in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Max retries reached for {case['test_name']}. Moving to next test case.")
        time.sleep(2)


def deploy_test_runner(node_count):
    deployment_file = 'configs/k8s/minik/default/deployment/tests_runner_d.yaml'

    if not os.path.exists(deployment_file):
        current_directory = os.getcwd()
        dir_contents = os.listdir(current_directory)
        error_message = (
            f"Deployment file '{deployment_file}' does not exist in the current directory: {current_directory}!\n"
            f"Contents of the current directory:\n{dir_contents}")
        print(error_message)
        raise FileNotFoundError(error_message)

    print(f"Deploying {node_count} replicas of the test-runner...")

    with open(deployment_file, 'r') as f:
        deployment_yaml = f.read()

    deployment_yaml = deployment_yaml.replace("{{node_count}}", str(node_count))

    with open(deployment_file, 'w') as f:
        f.write(deployment_yaml)

    subprocess.run(["kubectl", "apply", "-f", deployment_file], check=True)
    print(f"Deployment with {node_count} replicas applied.")


if __name__ == "__main__":
    print("Starting Test Case Controller...")

    try:
        deploy_test_runner(node_count)

        while not is_test_runner_ready():
            print("Waiting for Test Runner to be ready...")
            time.sleep(RETRY_DELAY)

        send_test_cases()
        print("All test cases sent.")

    except FileNotFoundError as e:
        print(f"Error: {e}")

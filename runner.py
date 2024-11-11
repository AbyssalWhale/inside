from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess


class TestRunnerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        test_case = json.loads(post_data)

        # Extract test name and marker from the received test case
        test_name = test_case.get("test_name")
        marker = test_case.get("marker", "regression")  # Default to "regression" if marker is not provided

        # Construct the pytest command to include the marker for regression
        print(f"Running test: {test_name} with marker: {marker}")
        pytest_command = [
            "pytest", "-m", marker,
            "--junitxml=/app/tests-results/junit-test-results.xml"
        ]

        # Run the pytest command
        subprocess.run(pytest_command)

        self.send_response(200)
        self.end_headers()


server_address = ('', 8080)
httpd = HTTPServer(server_address, TestRunnerHandler)
print("Test Runner listening on port 8080...")
httpd.serve_forever()
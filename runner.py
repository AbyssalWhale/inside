from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

class TestRunnerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        test_case = json.loads(post_data)

        test_name = test_case.get("test_name")
        marker = test_case.get("marker", "regression")

        logging.info(f"Running test: {test_name} with marker: {marker}")
        pytest_command = [
            "pytest", "-m", marker,
            "--junitxml=/app/tests-results/junit-test-results.xml"
        ]

        try:
            # Run the pytest command and capture output
            result = subprocess.run(pytest_command, capture_output=True, text=True)

            # Log the pytest output
            logging.info(f"pytest output:\n{result.stdout}")
            logging.error(f"pytest error:\n{result.stderr}")

            if result.returncode != 0:
                logging.error(f"Test execution failed for {test_name} with marker {marker}")
                self.send_response(500)  # Internal server error if pytest fails
            else:
                logging.info(f"Test {test_name} executed successfully.")
                self.send_response(200)  # Success response
        except Exception as e:
            logging.error(f"Error running pytest: {str(e)}")
            self.send_response(500)

        self.end_headers()


server_address = ('', 8080)
httpd = HTTPServer(server_address, TestRunnerHandler)
logging.info("Test Runner listening on port 8080...")
httpd.serve_forever()
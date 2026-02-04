"""
Playwright test configuration.
Starts the Flask server before tests and stops it after.
"""

import pytest
import subprocess
import time
import sys
import os
import requests

# Must use port 5001 because the frontend JS hardcodes API_BASE_URL to localhost:5001
SERVER_PORT = 5001
BASE_URL = f"http://localhost:{SERVER_PORT}"

# Path to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LAUNCHER = os.path.join(PROJECT_ROOT, "tests", "_test_server.py")
LOG_DIR = os.path.join(PROJECT_ROOT, "tests")


@pytest.fixture(scope="session")
def _server():
    """Start the Flask server as a subprocess for the test session."""
    stdout_log = open(os.path.join(LOG_DIR, "server_stdout.log"), "w")
    stderr_log = open(os.path.join(LOG_DIR, "server_stderr.log"), "w")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    server_process = subprocess.Popen(
        [sys.executable, "-u", LAUNCHER, str(SERVER_PORT)],
        stdout=stdout_log,
        stderr=stderr_log,
        env=env,
    )

    # Wait for server to be ready
    for _ in range(30):
        try:
            resp = requests.get(f"{BASE_URL}/")
            if resp.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        if server_process.poll() is not None:
            stdout_log.close()
            stderr_log.close()
            raise RuntimeError("Flask server exited prematurely.")
        time.sleep(0.5)
    else:
        server_process.terminate()
        stdout_log.close()
        stderr_log.close()
        raise RuntimeError("Flask server failed to start within 15s.")

    yield server_process

    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
    stdout_log.close()
    stderr_log.close()


@pytest.fixture(scope="session")
def base_url(_server):
    """Provide the base URL for Playwright tests."""
    return BASE_URL


@pytest.fixture
def home_page(page, base_url):
    """Navigate to the home page and wait for books to load."""
    page.goto(base_url)
    # Wait for the books table to render
    page.wait_for_selector("#books-table-container table", timeout=10000)
    return page

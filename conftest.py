import pytest
import json
from helpers.api_client import APIClient
from datetime import datetime
from jinja2 import Template
import os

# -------------------------------------------------
# Helper: Safe JSON Loader
# -------------------------------------------------
def safe_load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[CONFIG ERROR] Could not load {path}: {e}")
        return None


# -------------------------------------------------
# CLI Option for manual config
# -------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--config",
        action="store",
        default="configs/simple_bet.json",
        help="Path to configuration file"
    )


# -------------------------------------------------
# Fixture: Load config dynamically (function scope)
# -------------------------------------------------
@pytest.fixture(scope="function")
def load_config(pytestconfig, request):

    test_name = request.node.name.lower()

    # Auto detect config file by test name
    if "simple" in test_name:
        config_path = "configs/simple_bet.json"
    elif "combo" in test_name:
        config_path = "configs/combo_bet.json"
    elif "error" in test_name or "validation" in test_name:
        config_path = "configs/error_flow.json"
    else:
        # Fallback to CLI option
        config_path = pytestconfig.getoption("config")

    print(f"[CONFIG] Loading config: {config_path}")
    config_data = safe_load_json(config_path)

    # Fallback if config fails
    if config_data is None:
        fallback = "configs/error_flow.json"
        print(f"[CONFIG WARNING] Falling back to {fallback}")
        config_data = safe_load_json(fallback)

        if config_data is None:
            raise RuntimeError("❌ Could not load main config or fallback config.")

    return config_data


# -------------------------------------------------
# Fixture: API Client (function scope)
# -------------------------------------------------
@pytest.fixture(scope="function")
def api_client(load_config):
    client = APIClient(load_config["base_url"])
    username = load_config["auth"]["username"]
    password = load_config["auth"]["password"]

    # Try to generate token (error flow may not require it)
    try:
        token = client.generate_token(username, password)
        client.token = token
    except Exception:
        client.token = None

    return client


@pytest.fixture(scope="function")
def auth_token(api_client):
    return api_client.token


# -------------------------------------------------
# Reporting system
# -------------------------------------------------
os.makedirs("reports", exist_ok=True)
results = []


def pytest_runtest_logreport(report):
    if report.when == "call":
        try:
            parameters = report.nodeid.split("[")[1].rstrip("]")
        except IndexError:
            parameters = None

        result = {
            "test_name": report.nodeid.split("[")[0],
            "status": report.outcome,
            "execution_time": report.duration,
            "parameters": parameters,
            "failure_details": str(report.longrepr) if report.failed else None
        }

        results.append(result)


def pytest_sessionfinish(session, exitstatus):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_path = f"reports/test_report_{timestamp}.json"
    html_path = f"reports/test_report_{timestamp}.html"

    summary = {
        "total": session.testscollected,
        "passed": len([r for r in results if r["status"] == "passed"]),
        "failed": len([r for r in results if r["status"] == "failed"])
    }

    final_report = {"summary": summary, "tests": results}

    # Save JSON
    with open(json_path, "w") as f:
        json.dump(final_report, f, indent=4)

    # HTML Template
    template_str = """
    <html>
    <head>
        <title>Test Report</title>
        <style>
            table {border-collapse: collapse; width: 100%; }
            th, td {border: 1px solid black; padding: 5px; text-align: left;}
            th {background-color: #f2f2f2;}
            .passed {background-color: #c6efce;}
            .failed {background-color: #ffc7ce;}
        </style>
    </head>
    <body>
        <h1>Test Report</h1>
        <p>Total: {{ summary.total }} | Passed: {{ summary.passed }} | Failed: {{ summary.failed }}</p>

        <table>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Execution Time</th>
                <th>Parameters</th>
                <th>Failure Details</th>
            </tr>
            {% for t in tests %}
            <tr class="{{ t.status }}">
                <td>{{ t.test_name }}</td>
                <td>{{ t.status }}</td>
                <td>{{ t.execution_time | round(3) }}</td>
                <td>{{ t.parameters }}</td>
                <td>{{ t.failure_details or '' }}</td>
            </tr>
            {% endfor %}
        </table>

    </body>
    </html>
    """

    html = Template(template_str).render(summary=summary, tests=results)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n📄 JSON Report: {json_path}")
    print(f"📄 HTML Report: {html_path}")

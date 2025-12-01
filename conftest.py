import pytest
import json
from helpers.api_client import APIClient
from datetime import datetime
from jinja2 import Template
import os

# --------------------------------------
# Fixture: Configuration from JSON
# --------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--config",
        action="store",
        default="configs/simple_bet.json",
        help="Ruta al archivo de configuración JSON"
    )

@pytest.fixture(scope="session")
def load_config(pytestconfig):
    config_file = pytestconfig.getoption("config")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

# --------------------------------------
# Fixture: APIClient
# --------------------------------------
@pytest.fixture(scope="session")
def api_client(load_config):
    client = APIClient(load_config["base_url"])
    username = load_config["auth"]["username"]
    password = load_config["auth"]["password"]
    
    # Generar token usando el endpoint correcto
    token = client.generate_token(username, password)
    
    client.token = token
    return client

# --------------------------------------
# Fixture optional
# --------------------------------------
@pytest.fixture(scope="session")
def auth_token(api_client):
    return api_client.token


os.makedirs("reports", exist_ok=True)

results = []

# Capture each test result
def pytest_runtest_logreport(report):
    if report.when == "call":
        # Try to get parameters if test is parameterized
        try:
            parameters = report.nodeid.split("[")[1].rstrip("]")
        except IndexError:
            parameters = None

        test_result = {
            "test_name": report.nodeid.split("[")[0],
            "status": report.outcome,
            "execution_time": report.duration,
            "parameters": parameters,
            "failure_details": None
        }

        if report.failed:
            test_result["failure_details"] = str(report.longrepr)

        results.append(test_result)


# Generate JSON and HTML after test session finishes
def pytest_sessionfinish(session, exitstatus):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_path = f"reports/test_report_{timestamp}.json"
    html_path = f"reports/test_report_{timestamp}.html"

    summary = {
        "total": session.testscollected,
        "passed": len([r for r in results if r['status'] == 'passed']),
        "failed": len([r for r in results if r['status'] == 'failed'])
    }

    report_data = {
        "summary": summary,
        "tests": results
    }

    # Save JSON report
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=4)

    # Generate HTML report
    template_str = """
    <html>
    <head>
        <title>Test Report</title>
        <style>
            table {border-collapse: collapse; width: 100%;}
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
                <th>Execution Time (s)</th>
                <th>Parameters</th>
                <th>Failure Details</th>
            </tr>
            {% for test in tests %}
            <tr class="{{ test.status }}">
                <td>{{ test.test_name }}</td>
                <td>{{ test.status }}</td>
                <td>{{ test.execution_time | round(3) }}</td>
                <td>{{ test.parameters }}</td>
                <td>{{ test.failure_details if test.failure_details else '' }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    template = Template(template_str)
    html_content = template.render(summary=summary, tests=results)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\nJSON report saved to {json_path}")
    print(f"HTML report saved to {html_path}")
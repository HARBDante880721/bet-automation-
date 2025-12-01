import pytest
import json
import os
from helpers.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():

    client = APIClient()
    token = client.authenticate()

    if not token:
        raise AssertionError("Authentication failed — token is empty.")

    return client


@pytest.fixture(scope="session")
def load_config(pytestconfig):
    """
    Loads the JSON config file passed through --config.
    Example:
        pytest --config configs/simple_bet.json
    """
    config_path = pytestconfig.getoption("--config")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        data = json.load(f)

    return data

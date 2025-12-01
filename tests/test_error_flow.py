import pytest
from helpers.api_client import APIClient

@pytest.mark.api
def test_error_validation_flow(api_client, load_config):
    invalid_fixture = load_config.get("invalid_fixture_id")
    invalid_market = load_config.get("invalid_market")

    response = api_client.get_odds(invalid_fixture, invalid_market)
    data = response.json()

    assert "detail" in data
    assert data["detail"] == "Not Found"

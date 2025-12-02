import pytest

@pytest.mark.api
def test_error_validation_flow(api_client, load_config):
    invalid_fixture = load_config["invalid_fixture_id"]
    invalid_market = load_config["invalid_market"]

    response = api_client.get_odds(invalid_fixture, invalid_market)
    data = response.json()

    assert response.status_code in [400, 404, 422], (
        f"Expected error, but got {response.status_code}: {data}"
    )

    assert any(
        key in data for key in ["detail", "message", "error"]
    ), f"No error message found. Response: {data}"

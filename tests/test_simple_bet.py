import pytest

@pytest.mark.smoke
@pytest.mark.api
def test_simple_bet_creation(api_client, load_config):

    # -----------------------------
    # Read config safely
    # -----------------------------
    stake = str(load_config["stake"])
    fixture_id = str(load_config["fixture_id"])
    market_type = load_config["market_type"]
    sport_id = str(load_config.get("sport_id", 1))
    tournament_id = str(load_config.get("tournament_id", 1))

    # -----------------------------
    # User Information
    # -----------------------------
    user_info = {
        "username": load_config["auth"]["username"],
        "userKey": "ABC123",
        "id": "1"
    }

    # -----------------------------
    # Request Payload
    # -----------------------------
    payload = {
        "user": user_info,
        "betInfo": {
            "fixtureId": fixture_id,
            "market": market_type,
            "stake": stake,
            "amount": stake,
            "betId": [
                {
                    "betId": "123",
                    "fixtureId": fixture_id,
                    "odd": "2.0",
                    "sportId": sport_id,
                    "tournamentId": tournament_id
                }
            ],
            "source": "web"
        }
    }

    # -----------------------------
    # Call API
    # -----------------------------
    response = api_client.place_single_bet(payload)

    # If response isn't JSON, avoid breaking
    try:
        data = response.json()
    except ValueError:
        data = {"error": "Invalid JSON response"}

    # -----------------------------
    # Assertions
    # -----------------------------
    assert response.status_code == 200, (
        f"Expected 200 OK but got {response.status_code}\n"
        f"Response: {data}"
    )

    # Optional: validate keys
    assert "betId" in data or "status" in data or "message" in data, (
        f"Response does not contain expected fields.\n"
        f"Response: {data}"
    )

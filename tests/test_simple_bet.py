import pytest

@pytest.mark.smoke
@pytest.mark.api
def test_simple_bet_creation(api_client, load_config):
    stake = load_config["stake"]
    fixture_id = str(load_config["fixture_id"])
    user_info = {
        "username": load_config["auth"]["username"],
        "userKey": "ABC123",
        "id": "1"
    }

    payload = {
        "user": user_info,
        "betInfo": {
            "fixtureId": fixture_id,
            "market": load_config["market_type"],
            "stake": str(stake),
            "amount": str(stake),
            "betId": [
                {
                    "betId": "123",
                    "fixtureId": fixture_id,
                    "odd": "2.0",
                    "sportId": str(load_config.get("sport_id", 1)),
                    "tournamentId": str(load_config.get("tournament_id", 1))
                }
            ],
            "source": "web"
        }
    }

    response = api_client.place_single_bet(payload)
    data = response.json()
    assert response.status_code == 200, f"La API no devolvió 200 OK: {data}"

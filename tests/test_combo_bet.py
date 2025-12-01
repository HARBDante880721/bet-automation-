import pytest

@pytest.mark.api
def test_combo_bet_flow(api_client, load_config):
    stake = load_config["stake"]
    selections = load_config["selections"]

    for sel in selections:
        payload = {
            "betInfo": {
                "fixtureId": str(sel["fixture_id"]),
                "market": sel["market"],
                "stake": str(stake),
                "amount": str(stake),
                "betId": str(sel.get("betId", "123")),  # string obligatorio
                "source": "web",
                "sportId": str(sel.get("sport_id", 1)),
                "tournamentId": str(sel.get("tournament_id", 1)),
                "odd": str(sel.get("odd", 2.0))
            },
            "betsAdded": []
        }

        resp = api_client.add_bet_to_combo(payload)
        data = resp.json()
        assert resp.status_code == 200, f"Fallo al agregar selección: {data}"

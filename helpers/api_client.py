import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.token = None

    # ====================================================
    # AUTH
    # ====================================================
    def generate_token(self, username, password):
        url = f"{self.base_url}/auth/generate_token"
        payload = {"username": username, "password": password}

        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()

            data = resp.json()
            self.token = data.get("token")

            return self.token

        except Exception as e:
            self.token = None
            print(f"[WARN] Token could not be generated: {e}")
            return None

    def _auth_headers(self):
        
        headers = {}
        if self.token:
            headers["token"] = self.token
        return headers

    # ====================================================
    # BALANCE
    # ====================================================
    def get_balance(self):
        url = f"{self.base_url}/balance"
        return requests.get(url, headers=self._auth_headers())

    # ====================================================
    # FIXTURES
    # ====================================================
    def get_fixtures(self, sport_id, tournament_id):
        url = f"{self.base_url}/fixtures"
        params = {"sport_id": sport_id, "tournament_id": tournament_id}
        return requests.get(url, params=params, headers=self._auth_headers())

    # ====================================================
    # ODDS
    # ====================================================
    def get_odds(self, fixture_id, market_type):
        url = f"{self.base_url}/odds"
        params = {"fixture_id": fixture_id, "market_type": market_type}
        return requests.get(url, params=params, headers=self._auth_headers())

    # ====================================================
    # SINGLE BET
    # ====================================================
    def place_single_bet(self, payload):
        url = f"{self.base_url}/place-bet"
        return requests.post(url, json=payload, headers=self._auth_headers())

    # ====================================================
    # COMBO BETS
    # ====================================================
    def add_bet_to_combo(self, payload):
        url = f"{self.base_url}/add-bet-to-combo"
        return requests.post(url, json=payload, headers=self._auth_headers())

    def get_combo_odds(self):
        url = f"{self.base_url}/get-combo-odds"
        return requests.post(url, headers=self._auth_headers())

    def place_combo_bet(self, stake):
        url = f"{self.base_url}/place-combo-bet"
        payload = {"stake": stake}
        return requests.post(url, json=payload, headers=self._auth_headers())

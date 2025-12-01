# Betting API Automation Tests

## Overview
This project contains automated tests for a betting API, including **single bets**, **combo bets**, and **error/robustness scenarios**.  
Tests are **parameterized** and generate **JSON and HTML reports** automatically.

---

## Installation

1. **Clone the repository:**

git clone https://github.com/your-username/Automation.git
cd Automation

2. **Create and activate a virtual environment:** 

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. **Install dependencies:** 

pip install -r requirements.txt

## Commands to run test

**Run all tests with default configuration:**

pytest --config configs/simple_bet.json


**Run a specific test file:**

pytest tests/test_simple_bet.py


**Run with verbose output:**

pytest -v --config configs/simple_bet.json

Note:
Reports will be saved automatically in the reports/ folder as JSON and HTML.

## Modifying Test Parameters

All configurable parameters are stored in JSON/YAML files inside configs/.

Example: configs/simple_bet.json:

{
  "base_url": "https://api.example.com",
  "credentials": {
    "username": "user",
    "password": "pass"
  },
  "sport_id": 1,
  "tournament_id": 101,
  "market_type": "win",
  "stake": 10,
  "combo_selections": [
    {"sport_id":1,"market":"win"},
    {"sport_id":2,"market":"spread"}
  ],
  "timeouts": 10,
  "retry_count": 2
}

To modify parameters, edit the JSON/YAML file or pass a different config:

pytest --config configs/my_custom_config.json

## Reporting

JSON Report: reports/test_report_<timestamp>.json
Contains detailed test execution data: status, parameters, execution time, failure details.

HTML Report: reports/test_report_<timestamp>.html
Color-coded pass/fail summary for easy visual inspection.

Notes

* Tests are fully parameterized, allowing multiple environments (dev, staging, prod).

* Concurrency/stress tests included for atomicity of balance updates.

* Ensure Jinja2 is installed to generate HTML reports.

Author

Alex Romero – QA Automation Engineer
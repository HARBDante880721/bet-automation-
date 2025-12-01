TEST PLAN – Betting Automation API Project
1. Introduction

This Test Plan describes the approach, scope, deliverables, and strategy for validating the Betting Automation API project.
The goal is to ensure API correctness, business logic accuracy, and reliable automated execution for multiple bet flows.

2. Deliverables

2.1 Test Plan (TEST_PLAN.md)

This document includes:

A. Endpoint Analysis

List of endpoints relevant to the betting flows and selected for testing:

Endpoint	Method	Purpose
/auth/login	POST	Generate authentication token
/balance	GET	Retrieve user balance
/fixtures?sport_id={id}&tournament_id={id}	GET	Returns fixtures for a sport/tournament
/odds?fixture_id={id}&market_type={type}	GET	Retrieves odds for markets
/place-bet	POST	Places a single bet
/add-bet-to-combo	POST	Adds selection to combo ticket
/get-combo-odds	POST	Calculates total combo odds
/place-combo-bet	POST	Places combo bet

B. Identified Test Cases

ID	Description	Priority	Type
TC01	Validate login and token generation	High	Positive
TC02	Get balance and validate JSON structure	Medium	Positive
TC03	Find fixture for sport/tournament	High	Positive
TC04	Retrieve odds for a market	High	Positive
TC05	Place a simple bet successfully	High	Positive
TC06	Combo bet: generate total odds	High	Positive
TC07	Error handling when placing invalid bet	Medium	Negative
TC08	Validate insufficient balance error	High	Negative
TC09	Validate odd changes before bet	Medium	Negative

C. E2E Flows to Automate

Three end-to-end flows will be automated:

Simple Bet Flow
Combo Bet Flow
Error Validation Flow

Example: placing a bet with insufficient balance or invalid market.

D. Parameterization Strategy

Configuration values must be read from an external file (JSON/YAML/CSV).
Parameters include:

Sport IDs

Tournament IDs

Market types

Stake amounts

Multiple selections for combo bets

User credentials (in environment variables)

3. Automation Framework

The automation code will contain:

Reusable helpers (API clients, data loaders, validators)

Pytest fixtures (authentication, configuration loading)

Test suites (simple, combo, negative)

Parameter files (JSON/YAML)

Directory example:

Automation/
│── test_cases/
│── test_suites/
│── configs/
│── utils/
│── reports/
│── logs/
│── TEST_PLAN.md

4. Reporting System

When tests finish, an automatic reporting system must generate:

* HTML Report

Test summary

Pass/fail results

Failure screenshots/logs (if UI exists)

Execution timestamps

* JSON Report Must Contain
Field	Description
tests_executed	Total number of tests
passed	Count of passed tests
failed	Count of failed tests
execution_time	Duration per test
failure_details	Expected vs actual
parameters_used	Data read from configuration file

Tools that can be used:

Pytest JSON report plugin

Pytest HTML plugin

5. TEST SPECIFICATIONS

* TEST 1: Simple Bet End-to-End (Parameterized)
Configuration Example (JSON)
{
  "sport_id": 1,
  "tournament_id": 101,
  "market_type": "1X2",
  "stake": 100.00
}

Test Flow

Authenticate (generate token)

Get initial balance

Find fixture for specified sport/tournament

Get odds for selected market

Place bet

Get final balance

Validate deductions

Validations

- Token generated successfully
- Balance deducted correctly

initial_balance - stake = final_balance
- bet_id returned
- Potential winnings calculated correctly

stake × odd

* TEST 2: Combo Bet (Parameterized)
Configuration Example
{
  "selections": [
    { "sport_id": 1, "market": "1X2" },
    { "sport_id": 1, "market": "Over/Under" },
    { "sport_id": 2, "market": "Spread" }
  ],
  "stake": 50.00
}

Test Flow

Authentication

Find fixtures for each selection

Add each selection to combo

Call /get-combo-odds

Validate manual calculation:

total_odd = odd1 × odd2 × odd3

Place combo bet

Validate final balance

Validations

- Calculated total odds = product of individual odds (± 0.01 tolerance)
- Potential winnings = stake × total_odd
- Balance updated correctly
- combo_bet_id returned

* TEST 3: Custom Test – Odd Change Validation (Important Scenario)
Purpose

Ensure that when an odd changes between selection and confirmation, the API responds correctly (usually rejecting or flagging the bet).

Test Flow

Authentication

Select a fixture and market

Retrieve current odd

Simulate odd change (mock or updated call)

Place bet with old odd value

Validate system behavior

Validations

- API must return an error if odd changed
- Error code should be consistent (e.g., ODD_CHANGED)
- Old and new odds must be returned in the response
- Bet must NOT be placed

6. Risks

Risk	Impact	Mitigation
Odds change quickly	High	Add retry & tolerance logic
API instability	Medium	Use retries + logging
Bad parameter data	Medium	Validate input schema
Authentication expires	Medium	Renew token fixture

7. Approval

This Test Plan must be approved by:

QA Engineer

QA Lead

Product Owner
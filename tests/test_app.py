from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root_returns_system_ready() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "System Ready"}


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_intake_accepts_valid_financial_profile() -> None:
    payload = {
        "monthly_income": 4200,
        "debt_balance": 9500,
        "savings_goal": 300,
        "financial_goal": "Build an emergency fund",
        "expenses": {
            "housing": 1200,
            "utilities": 180,
            "food": 450,
            "transportation": 240,
            "healthcare": 125,
            "debt_payments": 300,
            "personal": 175,
            "other": 130,
        },
    }

    response = client.post("/intake", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Thanks for sharing your numbers. We can build from here."
    assert response.json()["summary"] == {
        "monthly_income": 4200.0,
        "total_expenses": 2800.0,
        "remaining_balance": 1400.0,
        "spending_ratio": 66.7,
        "debt_balance": 9500.0,
        "savings_goal": 300.0,
    }


def test_intake_rejects_negative_values() -> None:
    payload = {
        "monthly_income": 3000,
        "debt_balance": -50,
        "savings_goal": 100,
        "financial_goal": "Catch up on bills",
        "expenses": {
            "housing": 1200,
            "utilities": 150,
            "food": 350,
            "transportation": 220,
            "healthcare": 80,
            "debt_payments": 175,
            "personal": 100,
            "other": 60,
        },
    }

    response = client.post("/intake", json=payload)

    assert response.status_code == 422

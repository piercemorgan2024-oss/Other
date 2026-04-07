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
            "gas": 240,
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
        "total_expenses": 2675.0,
        "remaining_balance": 1525.0,
        "spending_ratio": 63.7,
        "debt_balance": 9500.0,
        "savings_goal": 300.0,
    }
    assert response.json()["budget_plan"]["recommended_budget"] == {
        "categories": {
            "housing": 1260.0,
            "utilities": 420.0,
            "food": 504.0,
            "gas": 420.0,
            "debt_payments": 420.0,
            "personal": 210.0,
            "other": 210.0,
        },
        "savings": 300.0,
        "essentials_total": 2370.0,
        "flexible_total": 305.0,
    }
    assert response.json()["budget_plan"]["budget_health"]["status"] == "stable"
    assert response.json()["spending_analysis"]["pressure_level"] == "low"
    assert response.json()["spending_analysis"]["overspending_categories"] == []
    assert response.json()["recommendations"]["recommendations"][0]["title"] == "Use your current stability intentionally"
    assert any(
        "savings" in recommendation["action"].lower()
        for recommendation in response.json()["recommendations"]["recommendations"]
    )


def test_intake_handles_irregular_low_income_profile() -> None:
    payload = {
        "monthly_income": 1800,
        "debt_balance": 3200,
        "savings_goal": 200,
        "financial_goal": "Stay current on bills",
        "expenses": {
            "housing": 760,
            "utilities": 135,
            "food": 240,
            "gas": 120,
            "debt_payments": 150,
            "personal": 80,
            "other": 160,
        },
    }

    response = client.post("/intake", json=payload)

    assert response.status_code == 200
    assert response.json()["budget_plan"]["recommended_budget"]["savings"] == 155.0
    assert response.json()["budget_plan"]["budget_health"]["status"] == "tight"
    assert response.json()["spending_analysis"]["pressure_level"] == "moderate"
    assert response.json()["spending_analysis"]["pressure_points"][-1]["title"] == "Savings goal does not have full room yet"
    assert response.json()["recommendations"]["recommendations"][0]["title"] == "Free up a small monthly cushion"


def test_intake_handles_high_debt_profile_with_negative_balance() -> None:
    payload = {
        "monthly_income": 2600,
        "debt_balance": 18000,
        "savings_goal": 150,
        "financial_goal": "Reduce debt stress",
        "expenses": {
            "housing": 1100,
            "utilities": 210,
            "food": 390,
            "gas": 230,
            "debt_payments": 420,
            "personal": 180,
            "other": 140,
        },
    }

    response = client.post("/intake", json=payload)

    assert response.status_code == 200
    assert response.json()["summary"]["remaining_balance"] == -70.0
    assert response.json()["budget_plan"]["budget_health"]["status"] == "stretched"
    assert response.json()["budget_plan"]["adjustments"][0]["category"] == "housing"
    assert response.json()["spending_analysis"]["pressure_level"] == "high"
    assert response.json()["spending_analysis"]["overspending_categories"][0]["category"] == "housing"
    assert response.json()["spending_analysis"]["relief_areas"][0]["label"] == "Housing"
    assert response.json()["recommendations"]["recommendations"][0]["title"] == "Create breathing room first"
    assert "housing" in response.json()["recommendations"]["next_step"].lower()


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
            "gas": 220,
            "debt_payments": 175,
            "personal": 100,
            "other": 60,
        },
    }

    response = client.post("/intake", json=payload)

    assert response.status_code == 422

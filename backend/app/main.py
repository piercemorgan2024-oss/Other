from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.analysis_engine import build_spending_analysis
from backend.app.budget_engine import build_budget_plan
from backend.app.models import FinancialProfile, ScenarioRequest
from backend.app.recommendation_engine import build_recommendations
from backend.app.scenario_engine import apply_scenario


app = FastAPI(
    title="Smart Budget Advisor",
    description="Backend API for the Smart Budget Advisor MVP.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "System Ready"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def build_profile_response(profile: FinancialProfile, message: str) -> dict[str, object]:
    total_expenses = sum(profile.expenses.model_dump().values())
    remaining_balance = round(profile.monthly_income - total_expenses, 2)
    budget_plan = build_budget_plan(profile)
    spending_analysis = build_spending_analysis(profile)
    recommendations = build_recommendations(profile, budget_plan, spending_analysis)

    if profile.monthly_income == 0:
        spending_ratio = 0.0
    else:
        spending_ratio = round((total_expenses / profile.monthly_income) * 100, 1)

    return {
        "message": message,
        "profile": profile.model_dump(),
        "summary": {
            "monthly_income": profile.monthly_income,
            "total_expenses": round(total_expenses, 2),
            "remaining_balance": remaining_balance,
            "spending_ratio": spending_ratio,
            "debt_balance": profile.debt_balance,
            "savings_goal": profile.savings_goal,
        },
        "budget_plan": budget_plan,
        "spending_analysis": spending_analysis,
        "recommendations": recommendations,
    }


@app.post("/intake")
def submit_intake(profile: FinancialProfile) -> dict[str, object]:
    return build_profile_response(profile, "Thanks for sharing your numbers. We can build from here.")


@app.post("/scenario")
def run_scenario(request: ScenarioRequest) -> dict[str, object]:
    updated_profile = apply_scenario(
        request.profile,
        income_change=request.adjustments.monthly_income_change,
        savings_goal_change=request.adjustments.savings_goal_change,
        expense_changes={
            "housing": request.adjustments.housing_change,
            "utilities": request.adjustments.utilities_change,
            "food": request.adjustments.food_change,
            "gas": request.adjustments.gas_change,
            "debt_payments": request.adjustments.debt_payments_change,
            "personal": request.adjustments.personal_change,
            "other": request.adjustments.other_change,
        },
    )
    return build_profile_response(
        updated_profile,
        "Here is how those changes could affect your monthly picture.",
    )

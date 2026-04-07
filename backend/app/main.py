from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.models import FinancialProfile


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


@app.post("/intake")
def submit_intake(profile: FinancialProfile) -> dict[str, object]:
    total_expenses = sum(profile.expenses.model_dump().values())
    remaining_balance = round(profile.monthly_income - total_expenses, 2)

    if profile.monthly_income == 0:
        spending_ratio = 0.0
    else:
        spending_ratio = round((total_expenses / profile.monthly_income) * 100, 1)

    return {
        "message": "Thanks for sharing your numbers. We can build from here.",
        "profile": profile.model_dump(),
        "summary": {
            "monthly_income": profile.monthly_income,
            "total_expenses": round(total_expenses, 2),
            "remaining_balance": remaining_balance,
            "spending_ratio": spending_ratio,
            "debt_balance": profile.debt_balance,
            "savings_goal": profile.savings_goal,
        },
    }

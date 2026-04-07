from backend.app.budget_engine import BUDGET_TARGETS
from backend.app.models import FinancialProfile


def _round_money(value: float) -> float:
    return round(value, 2)


def _label(category: str) -> str:
    return category.replace("_", " ").title()


def build_spending_analysis(profile: FinancialProfile) -> dict[str, object]:
    expenses = profile.expenses.model_dump()
    monthly_income = profile.monthly_income
    total_expenses = sum(expenses.values())
    remaining_balance = monthly_income - total_expenses

    overspending_categories: list[dict[str, object]] = []
    for category, ratio in BUDGET_TARGETS.items():
        target_amount = monthly_income * ratio
        actual_amount = expenses[category]
        over_amount = actual_amount - target_amount

        if over_amount > 0:
            overspending_categories.append(
                {
                    "category": category,
                    "label": _label(category),
                    "current": _round_money(actual_amount),
                    "target": _round_money(target_amount),
                    "over_by": _round_money(over_amount),
                }
            )

    if remaining_balance < 0:
        pressure_level = "high"
        overview = "Your budget is carrying real pressure right now, so the best first move is to lower the biggest strains."
    elif monthly_income > 0 and total_expenses / monthly_income >= 0.85:
        pressure_level = "moderate"
        overview = "Most of your income is already committed, so even small reductions in key areas could create more stability."
    else:
        pressure_level = "low"
        overview = "Your spending is not showing immediate crisis pressure, which creates space to improve gradually."

    pressure_points = []
    if overspending_categories:
        pressure_points.extend(
            {
                "title": f"{item['label']} is above the starting target",
                "detail": f"About ${item['over_by']:.2f} could be redirected here over time.",
            }
            for item in overspending_categories[:3]
        )

    if remaining_balance < 0:
        pressure_points.append(
            {
                "title": "Monthly cash flow is negative",
                "detail": f"Expenses are running about ${abs(remaining_balance):.2f} above income.",
            }
        )
    elif remaining_balance < profile.savings_goal:
        pressure_points.append(
            {
                "title": "Savings goal does not have full room yet",
                "detail": "A few focused changes could help create more room for the goal you set.",
            }
        )

    relief_areas = [
        {
            "category": item["category"],
            "label": item["label"],
            "relief_amount": item["over_by"],
        }
        for item in overspending_categories[:3]
    ]

    return {
        "pressure_level": pressure_level,
        "overview": overview,
        "overspending_categories": overspending_categories,
        "pressure_points": pressure_points,
        "relief_areas": relief_areas,
    }

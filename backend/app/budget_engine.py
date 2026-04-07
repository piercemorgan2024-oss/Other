from backend.app.models import FinancialProfile


BUDGET_TARGETS = {
    "housing": 0.30,
    "utilities": 0.10,
    "food": 0.12,
    "gas": 0.10,
    "debt_payments": 0.10,
    "personal": 0.05,
    "other": 0.05,
}

ESSENTIAL_CATEGORIES = {
    "housing",
    "utilities",
    "food",
    "gas",
    "debt_payments",
}


def _round_money(value: float) -> float:
    return round(value, 2)


def _category_label(key: str) -> str:
    return key.replace("_", " ").title()


def build_budget_plan(profile: FinancialProfile) -> dict[str, object]:
    expenses = profile.expenses.model_dump()
    monthly_income = profile.monthly_income
    total_expenses = sum(expenses.values())
    available_after_expenses = monthly_income - total_expenses

    if monthly_income <= 0:
        savings_recommendation = 0.0
    else:
        target_savings = min(profile.savings_goal, monthly_income * 0.20)
        savings_recommendation = max(0.0, min(target_savings, available_after_expenses))

    planned_categories: dict[str, float] = {}
    adjustments: list[dict[str, object]] = []

    for category, target_ratio in BUDGET_TARGETS.items():
        recommended = _round_money(monthly_income * target_ratio)
        actual = expenses[category]
        difference = _round_money(actual - recommended)
        planned_categories[category] = recommended

        if difference > 0:
            adjustments.append(
                {
                    "category": category,
                    "label": _category_label(category),
                    "current": actual,
                    "recommended": recommended,
                    "difference": difference,
                    "direction": "reduce",
                }
            )

    if available_after_expenses < 0:
        financial_health = "stretched"
        focus_message = "Your current expenses are above your income, so the first goal is finding breathing room."
    elif available_after_expenses < profile.savings_goal:
        financial_health = "tight"
        focus_message = "You are covering expenses, and a few targeted changes could free up more room for your goal."
    else:
        financial_health = "stable"
        focus_message = "You already have room to work with, which gives you a strong starting point."

    essentials_total = _round_money(sum(expenses[name] for name in ESSENTIAL_CATEGORIES))
    flexible_total = _round_money(total_expenses - essentials_total)

    return {
        "recommended_budget": {
            "categories": planned_categories,
            "savings": _round_money(savings_recommendation),
            "essentials_total": essentials_total,
            "flexible_total": flexible_total,
        },
        "budget_health": {
            "status": financial_health,
            "focus_message": focus_message,
            "available_after_expenses": _round_money(available_after_expenses),
        },
        "adjustments": sorted(adjustments, key=lambda item: item["difference"], reverse=True),
    }

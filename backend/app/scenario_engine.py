from backend.app.models import ExpenseBreakdown, FinancialProfile


def apply_scenario(
    profile: FinancialProfile,
    income_change: float = 0.0,
    savings_goal_change: float = 0.0,
    expense_changes: dict[str, float] | None = None,
) -> FinancialProfile:
    expense_changes = expense_changes or {}
    current_expenses = profile.expenses.model_dump()

    updated_expenses = {}
    for category, amount in current_expenses.items():
        adjusted = amount + expense_changes.get(category, 0.0)
        updated_expenses[category] = max(0.0, round(adjusted, 2))

    updated_income = max(0.0, round(profile.monthly_income + income_change, 2))
    updated_savings_goal = max(0.0, round(profile.savings_goal + savings_goal_change, 2))

    return FinancialProfile(
        monthly_income=updated_income,
        debt_balance=profile.debt_balance,
        savings_goal=updated_savings_goal,
        financial_goal=profile.financial_goal,
        expenses=ExpenseBreakdown(**updated_expenses),
    )

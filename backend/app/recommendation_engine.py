from backend.app.models import FinancialProfile


def build_recommendations(
    profile: FinancialProfile,
    budget_plan: dict[str, object],
    spending_analysis: dict[str, object],
) -> dict[str, object]:
    budget_health = budget_plan["budget_health"]
    recommended_budget = budget_plan["recommended_budget"]
    pressure_level = spending_analysis["pressure_level"]
    relief_areas = spending_analysis["relief_areas"]
    adjustments = budget_plan["adjustments"]

    recommendations: list[dict[str, str]] = []

    if pressure_level == "high":
        recommendations.append(
            {
                "title": "Create breathing room first",
                "action": "Focus on lowering one or two of the biggest monthly costs before pushing hard on every goal at once.",
                "reason": "When monthly cash flow is negative, the first win is getting back to a sustainable baseline.",
            }
        )
    elif pressure_level == "moderate":
        recommendations.append(
            {
                "title": "Free up a small monthly cushion",
                "action": "Aim to reduce one pressure point enough to create a little more space each month.",
                "reason": "Even modest room in the budget can make bills and savings goals feel more manageable.",
            }
        )
    else:
        recommendations.append(
            {
                "title": "Use your current stability intentionally",
                "action": "Keep your strongest habits in place and direct part of your available balance toward your main goal.",
                "reason": "You already have some margin, so consistency can build momentum quickly.",
            }
        )

    if relief_areas:
        top_area = relief_areas[0]
        recommendations.append(
            {
                "title": f"Start with {top_area['label']}",
                "action": f"Look for a realistic way to bring {top_area['label'].lower()} down by about ${top_area['relief_amount']:.2f} over time.",
                "reason": f"This category appears to offer the clearest opportunity for monthly relief right now.",
            }
        )

    savings_target = recommended_budget["savings"]
    if savings_target > 0:
        recommendations.append(
            {
                "title": "Protect a steady savings step",
                "action": f"Set aside about ${savings_target:.2f} a month as your current working savings target.",
                "reason": "A smaller repeatable step is more durable than an aggressive target that strains the month.",
            }
        )
    else:
        recommendations.append(
            {
                "title": "Pause savings pressure temporarily",
                "action": "Give yourself permission to stabilize bills and cash flow before expecting savings progress.",
                "reason": "Reducing stress and getting current can be the right first milestone.",
            }
        )

    if profile.debt_balance > 0:
        debt_payment_target = recommended_budget["categories"]["debt_payments"]
        recommendations.append(
            {
                "title": "Keep debt payments visible",
                "action": f"Plan around roughly ${debt_payment_target:.2f} for debt payments while you work on lowering other pressure points.",
                "reason": "Keeping debt in the plan helps prevent it from becoming invisible or snowballing further.",
            }
        )

    if adjustments:
        follow_up = adjustments[0]
        next_step = f"Review your {follow_up['label'].lower()} spending for one small change you could test this month."
    else:
        next_step = "Keep tracking your current categories and look for one habit that supports your goal consistently."

    return {
        "summary": budget_health["focus_message"],
        "recommendations": recommendations[:4],
        "next_step": next_step,
    }

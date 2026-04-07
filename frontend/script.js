const budgetForm = document.querySelector("#budget-form");
const scenarioForm = document.querySelector("#scenario-form");
const formMessage = document.querySelector("#form-message");
const scenarioMessage = document.querySelector("#scenario-message");
const resultCard = document.querySelector("#result-card");
const totalExpenses = document.querySelector("#total-expenses");
const remainingBalance = document.querySelector("#remaining-balance");
const spendingRatio = document.querySelector("#spending-ratio");
const goalText = document.querySelector("#goal-text");
const recommendedSavings = document.querySelector("#recommended-savings");
const essentialTotal = document.querySelector("#essential-total");
const flexibleTotal = document.querySelector("#flexible-total");
const focusMessage = document.querySelector("#focus-message");
const budgetHealth = document.querySelector("#budget-health");
const adjustmentList = document.querySelector("#adjustment-list");
const pressureLevel = document.querySelector("#pressure-level");
const analysisOverview = document.querySelector("#analysis-overview");
const pressurePoints = document.querySelector("#pressure-points");
const reliefAreas = document.querySelector("#relief-areas");
const recommendationSummary = document.querySelector("#recommendation-summary");
const recommendationList = document.querySelector("#recommendation-list");
const nextStepText = document.querySelector("#next-step-text");
const apiBaseUrl = "http://127.0.0.1:8000";
let currentProfile = null;

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

function parseRequiredNumber(formData, fieldName) {
  const rawValue = formData.get(fieldName);

  if (rawValue === null || rawValue === "") {
    throw new Error("Please complete every field before continuing.");
  }

  const value = Number(rawValue);

  if (Number.isNaN(value) || value < 0) {
    throw new Error("Please use zero or a positive number for all money fields.");
  }

  return value;
}

function parseScenarioNumber(formData, fieldName) {
  const rawValue = formData.get(fieldName);

  if (rawValue === null || rawValue === "") {
    return 0;
  }

  const value = Number(rawValue);

  if (Number.isNaN(value)) {
    throw new Error("Please use numeric values in the what-if tool.");
  }

  return value;
}

function buildPayload(formData) {
  const financialGoal = String(formData.get("financial_goal") || "").trim();

  if (!financialGoal) {
    throw new Error("Please share a financial goal so the tool can guide you.");
  }

  return {
    monthly_income: parseRequiredNumber(formData, "monthly_income"),
    debt_balance: parseRequiredNumber(formData, "debt_balance"),
    savings_goal: parseRequiredNumber(formData, "savings_goal"),
    financial_goal: financialGoal,
    expenses: {
      housing: parseRequiredNumber(formData, "housing"),
      utilities: parseRequiredNumber(formData, "utilities"),
      food: parseRequiredNumber(formData, "food"),
      gas: parseRequiredNumber(formData, "gas"),
      debt_payments: parseRequiredNumber(formData, "debt_payments"),
      personal: parseRequiredNumber(formData, "personal"),
      other: parseRequiredNumber(formData, "other"),
    },
  };
}

function renderAdjustments(adjustments) {
  adjustmentList.innerHTML = "";

  if (!adjustments.length) {
    const item = document.createElement("li");
    item.textContent = "Your current spending is already within the starting targets for each category.";
    adjustmentList.append(item);
    return;
  }

  adjustments.slice(0, 4).forEach((adjustment) => {
    const item = document.createElement("li");
    item.textContent = `${adjustment.label}: about ${formatCurrency(adjustment.difference)} above the starting target.`;
    adjustmentList.append(item);
  });
}

function renderSimpleList(listElement, items, emptyMessage) {
  listElement.innerHTML = "";

  if (!items.length) {
    const item = document.createElement("li");
    item.textContent = emptyMessage;
    listElement.append(item);
    return;
  }

  items.forEach((entry) => {
    const item = document.createElement("li");
    item.textContent = entry;
    listElement.append(item);
  });
}

function renderRecommendationList(recommendations) {
  recommendationList.innerHTML = "";

  if (!recommendations.length) {
    const item = document.createElement("li");
    item.textContent = "No recommendations are available yet.";
    recommendationList.append(item);
    return;
  }

  recommendations.forEach((recommendation) => {
    const item = document.createElement("li");
    item.textContent = `${recommendation.title}: ${recommendation.action} ${recommendation.reason}`;
    recommendationList.append(item);
  });
}

function renderResponse(data, messageElement) {
  messageElement.textContent = data.message;
  totalExpenses.textContent = formatCurrency(data.summary.total_expenses);
  remainingBalance.textContent = formatCurrency(data.summary.remaining_balance);
  spendingRatio.textContent = `${data.summary.spending_ratio}%`;
  goalText.textContent = data.profile.financial_goal;
  recommendedSavings.textContent = formatCurrency(data.budget_plan.recommended_budget.savings);
  essentialTotal.textContent = formatCurrency(data.budget_plan.recommended_budget.essentials_total);
  flexibleTotal.textContent = formatCurrency(data.budget_plan.recommended_budget.flexible_total);
  focusMessage.textContent = data.budget_plan.budget_health.focus_message;
  budgetHealth.textContent = `Status: ${data.budget_plan.budget_health.status}`;
  renderAdjustments(data.budget_plan.adjustments);
  pressureLevel.textContent = `Pressure level: ${data.spending_analysis.pressure_level}`;
  analysisOverview.textContent = data.spending_analysis.overview;
  renderSimpleList(
    pressurePoints,
    data.spending_analysis.pressure_points.map(
      (point) => `${point.title}. ${point.detail}`,
    ),
    "No major pressure points are standing out yet."
  );
  renderSimpleList(
    reliefAreas,
    data.spending_analysis.relief_areas.map(
      (area) => `${area.label}: around ${formatCurrency(area.relief_amount)} of potential monthly relief.`,
    ),
    "No overspending categories are above the current targets."
  );
  recommendationSummary.textContent = data.recommendations.summary;
  renderRecommendationList(data.recommendations.recommendations);
  nextStepText.textContent = data.recommendations.next_step;
  resultCard.hidden = false;
}

async function submitBudgetForm(event) {
  event.preventDefault();
  formMessage.classList.remove("error");
  resultCard.hidden = true;

  try {
    const formData = new FormData(budgetForm);
    const payload = buildPayload(formData);

    formMessage.textContent = "Saving your starting point...";

    const response = await fetch(`${apiBaseUrl}/intake`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("We could not save your information just yet. Please try again.");
    }

    const data = await response.json();
    currentProfile = data.profile;
    renderResponse(data, formMessage);
  } catch (error) {
    formMessage.textContent = error.message;
    formMessage.classList.add("error");
  }
}

async function submitScenarioForm(event) {
  event.preventDefault();
  scenarioMessage.classList.remove("error");

  if (!currentProfile) {
    scenarioMessage.textContent = "Save your starting point first so the what-if tool has a baseline.";
    scenarioMessage.classList.add("error");
    return;
  }

  try {
    const formData = new FormData(scenarioForm);
    const adjustments = {
      monthly_income_change: parseScenarioNumber(formData, "monthly_income_change"),
      savings_goal_change: parseScenarioNumber(formData, "savings_goal_change"),
      housing_change: parseScenarioNumber(formData, "housing_change"),
      utilities_change: parseScenarioNumber(formData, "utilities_change"),
      food_change: parseScenarioNumber(formData, "food_change"),
      gas_change: parseScenarioNumber(formData, "gas_change"),
      debt_payments_change: parseScenarioNumber(formData, "debt_payments_change"),
      personal_change: parseScenarioNumber(formData, "personal_change"),
      other_change: parseScenarioNumber(formData, "other_change"),
    };

    scenarioMessage.textContent = "Running your scenario...";

    const response = await fetch(`${apiBaseUrl}/scenario`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        profile: currentProfile,
        adjustments,
      }),
    });

    if (!response.ok) {
      throw new Error("We could not run that scenario yet. Please try again.");
    }

    const data = await response.json();
    renderResponse(data, scenarioMessage);
  } catch (error) {
    scenarioMessage.textContent = error.message;
    scenarioMessage.classList.add("error");
  }
}

budgetForm.addEventListener("submit", submitBudgetForm);
scenarioForm.addEventListener("submit", submitScenarioForm);

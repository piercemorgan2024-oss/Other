const apiStatus = document.querySelector("#api-status");
const budgetForm = document.querySelector("#budget-form");
const formMessage = document.querySelector("#form-message");
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
const apiBaseUrl = "http://127.0.0.1:8000";

async function loadStatus() {
  try {
    const response = await fetch(`${apiBaseUrl}/`);

    if (!response.ok) {
      throw new Error("Unable to reach backend");
    }

    const data = await response.json();
    apiStatus.textContent = data.message;
  } catch (error) {
    apiStatus.textContent = "Backend offline. Start the API to continue.";
  }
}

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
      transportation: parseRequiredNumber(formData, "transportation"),
      healthcare: parseRequiredNumber(formData, "healthcare"),
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

    formMessage.textContent = data.message;
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
    resultCard.hidden = false;
  } catch (error) {
    formMessage.textContent = error.message;
    formMessage.classList.add("error");
  }
}

loadStatus();
budgetForm.addEventListener("submit", submitBudgetForm);

const apiStatus = document.querySelector("#api-status");
const budgetForm = document.querySelector("#budget-form");
const formMessage = document.querySelector("#form-message");
const resultCard = document.querySelector("#result-card");
const totalExpenses = document.querySelector("#total-expenses");
const remainingBalance = document.querySelector("#remaining-balance");
const spendingRatio = document.querySelector("#spending-ratio");
const goalText = document.querySelector("#goal-text");
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
    resultCard.hidden = false;
  } catch (error) {
    formMessage.textContent = error.message;
    formMessage.classList.add("error");
  }
}

loadStatus();
budgetForm.addEventListener("submit", submitBudgetForm);

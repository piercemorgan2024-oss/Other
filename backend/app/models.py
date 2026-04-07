from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseBreakdown(BaseModel):
    housing: float = Field(ge=0)
    utilities: float = Field(ge=0)
    food: float = Field(ge=0)
    gas: float = Field(ge=0)
    debt_payments: float = Field(ge=0)
    personal: float = Field(ge=0)
    other: float = Field(ge=0)


class FinancialProfile(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    monthly_income: float = Field(ge=0)
    debt_balance: float = Field(ge=0)
    savings_goal: float = Field(ge=0)
    financial_goal: str = Field(min_length=1)
    expenses: ExpenseBreakdown

    @field_validator("financial_goal")
    @classmethod
    def goal_must_have_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Please share a financial goal so we can tailor the analysis.")
        return value


class ScenarioAdjustments(BaseModel):
    monthly_income_change: float = 0
    savings_goal_change: float = 0
    housing_change: float = 0
    utilities_change: float = 0
    food_change: float = 0
    gas_change: float = 0
    debt_payments_change: float = 0
    personal_change: float = 0
    other_change: float = 0


class ScenarioRequest(BaseModel):
    profile: FinancialProfile
    adjustments: ScenarioAdjustments

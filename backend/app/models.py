from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseBreakdown(BaseModel):
    housing: float = Field(ge=0)
    utilities: float = Field(ge=0)
    food: float = Field(ge=0)
    transportation: float = Field(ge=0)
    healthcare: float = Field(ge=0)
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

# Smart Budget Advisor User Guide

## What This Tool Does

Smart Budget Advisor helps a user:

- capture a simple monthly financial picture
- see a personalized budget summary
- spot spending pressure points
- review supportive next-step recommendations
- test small income or spending changes with the what-if tool

## How To Use It

1. Start the backend server.
2. Open `frontend/index.html` in a browser.
3. Enter monthly income, debt, savings goal, and expenses.
4. Select a clear financial goal.
5. Submit the form to view the budget, analysis, and recommendations.
6. Use the what-if tool to test one small change at a time.

## How To Read The Results

- `Current snapshot`: A quick look at monthly expenses, remaining balance, and overall spending ratio.
- `Recommended budget`: A starting monthly allocation and suggested savings target.
- `Spending analysis`: Areas creating the most pressure and possible relief points.
- `Recommendations`: Supportive next steps based on the user’s current situation.
- `What-if tool`: A way to test possible changes before making them in real life.

## Important Notes

- This tool is meant for planning and reflection, not professional financial advice.
- Approximate numbers are okay for a first pass.
- The MVP does not connect to banks or include taxes, investing, or advanced planning.

## Running The Project

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Then open `frontend/index.html`.

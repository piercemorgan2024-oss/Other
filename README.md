# Smart Budget Advisor

Smart Budget Advisor is a personal financial stability tool designed to help users build a personalized monthly budget, understand overspending patterns, and explore how small financial changes can improve long-term stability.

## Project Purpose

This project is guided by the project charter and project specs in this repository. The MVP focuses on:

- Personalized monthly budget generation
- Spending pattern analysis
- Overspending detection
- Actionable recommendations
- A what-if scenario engine

## Guiding Principles

- Clarity over complexity
- Accuracy over aesthetics
- User empowerment
- Transparency
- Modularity

## MVP Scope

Included:

- Budget generation
- Spending analysis
- Recommendation engine
- What-if scenario modeling
- Simple UI and basic documentation

Excluded:

- Bank integrations
- Mobile app
- Taxes, investments, or advanced financial planning
- Subscription or payment features

## Initial Tech Direction

- Frontend: HTML, CSS, JavaScript
- Backend: Python with Flask or FastAPI
- Data handling: In-memory for MVP

## Repository Notes

- `Project Charter.docx` contains the charter and scope.
- `Project Specs.docx` contains the functional and architectural guide.

This repository will be built incrementally with a focus on correctness, supportiveness, and maintainability.

## Project Structure

```text
backend/   FastAPI backend and business logic
frontend/  Static MVP interface
tests/     Automated tests
```

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the backend with `uvicorn backend.app.main:app --reload`.
4. Open `frontend/index.html` to view the initial UI shell.

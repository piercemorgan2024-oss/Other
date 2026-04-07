from fastapi import FastAPI


app = FastAPI(
    title="Smart Budget Advisor",
    description="Backend API for the Smart Budget Advisor MVP.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "System Ready"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

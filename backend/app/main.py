from fastapi import FastAPI

from backend.app.problems.router import router as problems_router
from backend.app.submissions.router import router as submissions_router


app = FastAPI(
    title="AI Coding & DSA Assessment Platform",
    version="0.1.0",
)


app.include_router(problems_router)
app.include_router(submissions_router)


@app.get("/")
def root():
    return {
        "message": "AI Coding & DSA Assessment Platform API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

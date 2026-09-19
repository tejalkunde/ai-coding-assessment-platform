from fastapi import FastAPI

app = FastAPI(
    title="AI Coding & DSA Assessment Platform",
    version="0.1.0",
)


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

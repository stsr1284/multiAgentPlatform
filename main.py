from fastapi import FastAPI
from orchestration_app.api.orchestration_router import router as orchestration_router

app = FastAPI(title="Multi-Agent-Platform", version="0.1.0")

app.include_router(orchestration_router, prefix="/orchestration")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

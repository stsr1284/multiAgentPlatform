from fastapi import FastAPI
from api.orchestration_router import router as orchestration_router

app = FastAPI(title="Orchestration App")

app.include_router(orchestration_router, prefix="/orchestration")
print("app size: ", app.__sizeof__())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("app size: ", app.__sizeof__())

from fastapi import FastAPI
from api.broker_router import router as broker_router

app = FastAPI(title="Broker App")

app.include_router(broker_router, prefix="/broker")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)

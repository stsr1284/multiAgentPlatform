from api.orchestration_router import router as orchestration_router
from contextlib import asynccontextmanager
from container import watcher, initialize_service
from shared.loggin_config import logger
from fastapi import FastAPI
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await initialize_service.setup_and_watcher_start()

    yield

    logger.info("Shutting down...")
    await initialize_service.stop()


app = FastAPI(title="Orchestration App", lifespan=lifespan)


app.include_router(orchestration_router, prefix="/orchestration")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

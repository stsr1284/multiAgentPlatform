from api.orchestration_router import router as orchestration_router
from contextlib import asynccontextmanager
from container import plugin_loader
from shared.loggin_config import logger
from fastapi import FastAPI
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("Starting up...")
    await plugin_loader.setup()
    asyncio.create_task(plugin_loader.watch())

    yield
    # shutdown
    logger.info("Shutting down...")


app = FastAPI(title="Orchestration App", lifespan=lifespan)


app.include_router(orchestration_router, prefix="/orchestration")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

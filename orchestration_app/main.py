from api.orchestration_router import router as orchestration_router
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from api.dependencies import get_initialize_service
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager
from shared.loggin_config import logger
from utils.config import settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    pool = AsyncConnectionPool(
        conninfo=settings.DB_URI,
        max_size=20,
        open=False,
        kwargs=settings.CONNECTION_KWARGS,
    )
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    app.state.db_pool = pool
    app.state.checkpointer = checkpointer
    initialize_service = get_initialize_service()
    await initialize_service.setup_and_watcher_start()

    yield

    await initialize_service.stop()
    await pool.close()
    logger.info("Shutting down...")


app = FastAPI(title="Orchestration App", lifespan=lifespan)

app.include_router(orchestration_router, prefix="/orchestration")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

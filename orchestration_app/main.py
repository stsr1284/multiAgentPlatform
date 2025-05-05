from api.orchestration_router import router as orchestration_router
from contextlib import asynccontextmanager
from container import initialize_service
from shared.loggin_config import logger
from fastapi import FastAPI

# test
from psycopg_pool import AsyncConnectionPool
from utils.config import settings
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    # test
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
    await initialize_service.setup_and_watcher_start()

    yield

    logger.info("Shutting down...")
    await initialize_service.stop()
    await pool.close()


app = FastAPI(title="Orchestration App", lifespan=lifespan)


app.include_router(orchestration_router, prefix="/orchestration")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

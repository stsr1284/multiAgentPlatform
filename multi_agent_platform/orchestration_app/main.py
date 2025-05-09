from api.orchestration_router import router as orchestration_router
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from api.dependencies import get_initialize_service
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(  # CORS 설정, 임시방편임
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ['http://localhost:3000', 'https://your-domain.com']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orchestration_router, prefix="/orchestration")

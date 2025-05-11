from api.orchestration_router import router as orchestration_router
from api.dependencies import get_initialize_service
from langgraph.checkpoint.memory import MemorySaver
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from shared.loggin_config import logger
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    app.state.checkpointer = MemorySaver()
    initialize_service = get_initialize_service()
    await initialize_service.setup_and_watcher_start()

    yield

    await initialize_service.stop()
    logger.info("Shutting down...")


app = FastAPI(title="Orchestration App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orchestration_router, prefix="/orchestration")

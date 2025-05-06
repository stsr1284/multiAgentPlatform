from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import ResumeAStreamStrategy
from application.orchestration_service import OrchestrationService
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from application.resume_service import ResumeService
from application import container
from fastapi import Request


def get_checkpointer(request: Request) -> AsyncPostgresSaver:
    return request.app.state.checkpointer


def get_orchestration_astream_strategy() -> OrchestrationAStreamStrategy:
    return container.orchestration_astream_strategy


def get_resume_astream_strategy() -> ResumeAStreamStrategy:
    return container.resume_astream_strategy


def get_orchestration_service() -> OrchestrationService:
    return container.orchestration_service


def get_resume_service() -> ResumeService:
    return container.resume_service

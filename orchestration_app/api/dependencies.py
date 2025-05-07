from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import ResumeAStreamStrategy
from domain.registry.agent_builder_registry import AgentBuilderRegistry
from domain.registry.orchestrator_registry import OrchestratorRegistry
from application.orchestration_service import OrchestrationService
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from application.InitializeService import InitializeService
from domain.registry.agent_registry import AgentRegistry
from domain.registry.graph_registry import GraphRegistry
from domain.registry.tool_registry import ToolRegistry
from application.resume_service import ResumeService
from domain.registry.llm_registry import LLMRegistry
from application import container
from fastapi import Request


def get_initialize_service() -> InitializeService:
    return container.initialize_service


def get_checkpointer(request: Request) -> AsyncPostgresSaver:
    return request.app.state.checkpointer


def get_llm_registry() -> LLMRegistry:
    return container.llm_registry


def get_tool_registry() -> ToolRegistry:
    return container.tool_registry


def get_agent_builder_registry() -> AgentBuilderRegistry:
    return container.agent_builder_registry


def get_agent_registry() -> AgentRegistry:
    return container.agent_registry


def get_orchestrator_registry() -> OrchestratorRegistry:
    return container.orchestrator_registry


def get_graph_registry() -> GraphRegistry:
    return container.graph_registry


def get_orchestration_astream_strategy() -> OrchestrationAStreamStrategy:
    return container.orchestration_astream_strategy


def get_resume_astream_strategy() -> ResumeAStreamStrategy:
    return container.resume_astream_strategy


def get_orchestration_service() -> OrchestrationService:
    return container.orchestration_service


def get_resume_service() -> ResumeService:
    return container.resume_service

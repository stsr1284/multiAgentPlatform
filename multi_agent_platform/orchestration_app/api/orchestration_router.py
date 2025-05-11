from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import (
    ResumeAStreamStrategy,
)
from domain.registry.agent_builder_registry import AgentBuilderRegistry
from domain.registry.orchestrator_registry import OrchestratorRegistry
from domain.entyties.user_input import OrchestrationInput, UserInput
from application.orchestration_service import OrchestrationService
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from domain.registry.agent_registry import AgentRegistry
from domain.registry.graph_registry import GraphRegistry
from domain.registry.tool_registry import ToolRegistry
from fastapi import APIRouter, Depends, HTTPException
from application.resume_service import ResumeService
from domain.registry.llm_registry import LLMRegistry
from fastapi.responses import StreamingResponse
from .dependencies import (
    get_orchestration_astream_strategy,
    get_resume_astream_strategy,
    get_agent_builder_registry,
    get_orchestrator_registry,
    get_orchestration_service,
    get_resume_service,
    get_agent_registry,
    get_graph_registry,
    get_tool_registry,
    get_checkpointer,
    get_llm_registry,
)
from langgraph.checkpoint.base import BaseCheckpointSaver

router = APIRouter()


@router.get("/get_tools")
async def get_tools(
    tool_registry: ToolRegistry = Depends(get_tool_registry),
):
    tools = await tool_registry.get_all()
    response = {key: value.description for key, value in tools.items()}
    return response


@router.get("/get_llms")
async def get_llms(
    llm_registry: LLMRegistry = Depends(get_llm_registry),
):
    llms = await llm_registry.get_all()
    return llms


@router.get("/get_builders")
async def get_builders(
    agent_builder_registry: AgentBuilderRegistry = Depends(get_agent_builder_registry),
):
    builders = await agent_builder_registry.get_all()
    response = [key for key in builders]
    return response


@router.get("/get_agents")
async def get_agents(
    agent_registry: AgentRegistry = Depends(get_agent_registry),
):
    agents = await agent_registry.get_all()
    response = [
        {"title": key, "description": value.description}
        for key, value in agents.items()
    ]
    return response


@router.get("/get_orchestrators")
async def get_orchestrators(
    orchestrator_registry: OrchestratorRegistry = Depends(get_orchestrator_registry),
):
    try:
        orchestrators = await orchestrator_registry.get_all()
        response = [
            {"title": key, "description": value.description}
            for key, value in orchestrators.items()
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/chat/astream")
async def run_orchestration(
    orchestration_input: OrchestrationInput,
    checkpointer: BaseCheckpointSaver = Depends(get_checkpointer),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    strategy: OrchestrationAStreamStrategy = Depends(
        get_orchestration_astream_strategy
    ),
):
    try:
        astream = await orchestration_service.run(
            strategy, orchestration_input, checkpointer
        )
        return StreamingResponse(astream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e


@router.post("/chat/astream_resume")
async def resume_orchestration(
    user_input: UserInput,
    resume_service: ResumeService = Depends(get_resume_service),
    strategy: ResumeAStreamStrategy = Depends(get_resume_astream_strategy),
):
    try:
        astream = await resume_service.run(strategy, user_input)
        return StreamingResponse(astream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

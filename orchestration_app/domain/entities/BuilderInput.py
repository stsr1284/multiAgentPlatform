from orchestration_app.domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from orchestration_app.domain.registry.LLMRegistry import LLMRegistry
from orchestration_app.domain.registry.ToolRegistry import ToolRegistry
from typing import List, Dict, Any, Union, Optional
from pydantic import BaseModel
from orchestration_app.domain.entities.AgentDefinition import AgentDefinition


class BaseOrchestartionBuilderInput(BaseModel):
    agentProfiles: List[Union[Dict[str, Any], AgentDefinition]]
    # agentBuilderRegistry: AgentBuilderRegistry
    # llmRegistry: LLMRegistry
    # toolRegistry: ToolRegistry


class SupervisorOrchestrationBuilderInput(BaseOrchestartionBuilderInput):
    llm: Optional[str] = None
    prompt: Optional[str] = None
    tools: Optional[List[str]] = None

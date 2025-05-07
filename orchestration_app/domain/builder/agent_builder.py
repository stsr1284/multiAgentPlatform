from domain.builder.base_orchestrator_workflow_builder import (
    BaseOrchestratorWorkflowBuilder,
)
from domain.registry.agent_builder_registry import AgentBuilderRegistry
from domain.registry.agent_registry import AgentRegistry
from domain.registry.tool_registry import ToolRegistry
from domain.registry.llm_registry import LLMRegistry
from .base_builder import BaseBuilder
from typing import Dict, Any
import copy


class AgentBuilder(BaseBuilder):
    def __init__(
        self,
        agent_builder_registry: AgentBuilderRegistry,
        llm_registry: LLMRegistry,
        tool_registry: ToolRegistry,
        agent_registry: AgentRegistry,
    ):
        super().__init__(agent_builder_registry, llm_registry, tool_registry)
        self.agent_registry = agent_registry

    async def build_from_json(self, json_data: str) -> None:
        agents = []
        if "agent_list" not in json_data:
            raise ValueError(
                "'agent_list' not found in JSON data. Please check the input format."
            )
        elif "agent_list" in json_data and not isinstance(
            json_data["agent_list"], list
        ):
            raise ValueError("'agent_list' must be a list")

        json_data = json_data["agent_list"]
        for idx, item in enumerate(json_data):
            try:
                if "agent" in item:
                    agent_data = item["agent"]
                    agent = await self.build_workflow(agent_data)
                    agents.append(agent)
                elif "orchestrator" in item:
                    orchestration_data = item["orchestrator"]
                    agent = await self.build_orchestration(orchestration_data)
                    agents.append(agent)
                else:
                    raise ValueError("Invalid item at index {idx}: {item}")
            except Exception as e:
                raise
        await self.agent_registry.reset(agents)

    async def build_orchestration(
        self, orchestration_data: Dict[str, Any]
    ) -> BaseOrchestratorWorkflowBuilder:
        try:
            if "type" not in orchestration_data or orchestration_data["type"] is None:
                raise ValueError("Missing 'type' in agent data")
            if "name" not in orchestration_data or orchestration_data["name"] is None:
                raise ValueError("Missing 'name' in agent data")
            if (
                "description" not in orchestration_data
                or orchestration_data["description"] is None
            ):
                raise ValueError("Missing 'description' in agent data")
            if (
                "agent_list" not in orchestration_data
                or orchestration_data["agent_list"] is None
            ):
                raise ValueError(
                    f"Missing 'agent_list' in orchestration data: {orchestration_data}"
                )
            agents = []
            for item in orchestration_data["agent_list"]:
                if "agent" in item:
                    agent = await self.build_workflow(item["agent"])
                    agents.append(agent)
                elif "orchestrator" in item:
                    agents.append(await self.build_orchestration(item["orchestrator"]))

                else:
                    raise ValueError(f"Invalid item in agent_list: {item}")

                if agents is None:
                    raise ValueError(
                        f"Agent list is empty in orchestration data: {orchestration_data}"
                    )
            orchestration_data_copy = copy.deepcopy(orchestration_data)
            builder = await self.build_workflow(orchestration_data_copy)
            [await builder.add_agent(agent) for agent in agents]
        except Exception as e:
            raise
        return builder

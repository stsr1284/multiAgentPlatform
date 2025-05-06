from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from domain.registry.ToolRegistry import ToolRegistry
from domain.registry.LLMRegistry import LLMRegistry
from typing import Any, Dict, List, Union
from shared.loggin_config import logger
from abc import ABC, abstractmethod
import copy


class BaseBuilder(ABC):
    def __init__(
        self,
        agent_builder_registry: AgentBuilderRegistry,
        llm_registry: LLMRegistry,
        tool_registry: ToolRegistry,
    ):
        self.agent_builder_registry = agent_builder_registry
        self.llm_registry = llm_registry
        self.tool_registry = tool_registry

    @abstractmethod
    async def build_from_json(self, data: str) -> None:
        pass

    async def build_workflow(self, agent_data: Dict[str, Any]) -> BaseWorkflowBuilder:
        try:
            if "type" not in agent_data:
                raise ValueError("Missing 'type' in agent data")
            if "name" not in agent_data:
                raise ValueError("Missing 'name' in agent data")
            if "description" not in agent_data:
                raise ValueError("Missing 'description' in agent data")

            builder = await self.agent_builder_registry.get(agent_data["type"])
            if not builder:
                raise ValueError(
                    f"Agent builder not found for type: {agent_data['type']}"
                )

            llm = await self._get_registry_item(
                agent_data.get("llm"), self.llm_registry, "LLM"
            )
            tools = await self._get_registry_item(
                agent_data.get("tool"), self.tool_registry, "Tool"
            )

            if agent_data.get("llm") and not llm:
                raise ValueError(f"LLM '{agent_data['llm']}' not found in registry")
            if agent_data.get("tool") and not tools:
                raise ValueError(f"Tool '{agent_data['tool']}' not found in registry")

            agent_data_copy = {
                k: v for k, v in agent_data.items() if k not in ("llm", "tool")
            }
            agent_data_copy = copy.deepcopy(agent_data_copy)
            if llm is not None:
                agent_data_copy["llm"] = llm
            if tools is not None:
                agent_data_copy["tool"] = tools
            await builder(**agent_data_copy)
        except Exception as e:
            logger.error(f"Error in build_agent: {e}")
            raise
        return builder

    async def _get_registry_item(
        self,
        input_data: Union[str, List[str]],
        registry: Dict[str, Any],
        type: str,
    ) -> List[Any]:
        if not input_data:
            return []
        item_names = [input_data] if isinstance(input_data, str) else input_data
        item_list = []

        for item_name in item_names:
            if not item_name:
                continue
            item = await registry.get(item_name)
            if not item:
                raise ValueError(f"{type} '{item_name}' not found in registry")
            item_list.append(item)

        return item_list

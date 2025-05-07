from domain.registry.agent_builder_registry import AgentBuilderRegistry
from domain.registry.orchestrator_registry import OrchestratorRegistry
from domain.registry.tool_registry import ToolRegistry
from domain.registry.llm_registry import LLMRegistry
from .base_builder import BaseBuilder


class OrchestratorBuilder(BaseBuilder):
    def __init__(
        self,
        agent_builder_registry: AgentBuilderRegistry,
        llm_registry: LLMRegistry,
        tool_registry: ToolRegistry,
        orchestrator_registry: OrchestratorRegistry,
    ):
        super().__init__(agent_builder_registry, llm_registry, tool_registry)
        self.orchestrator_registry = orchestrator_registry

    async def build_from_json(self, json_data: str) -> None:
        orchestrators = []
        if "orchestrator_list" not in json_data:
            raise ValueError(
                "'orchestrator_list' not found in JSON data. Please check the input format."
            )
        elif "orchestrator_list" in json_data and not isinstance(
            json_data["orchestrator_list"], list
        ):
            raise ValueError("'orchestrator_list' must be a list")

        json_data = json_data["orchestrator_list"]
        for idx, item in enumerate(json_data):
            try:
                if "orchestrator" in item:
                    orchestrator_data = item["orchestrator"]
                    orchestrator = await self.build_workflow(orchestrator_data)
                    orchestrators.append(orchestrator)
                else:
                    raise ValueError(
                        f"Invalid item format at index {idx}. Expected 'orchestrator' key."
                    )
            except Exception as e:
                raise ValueError(
                    f"Error creating orchestrator at index {idx}: {e}"
                ) from e
        await self.orchestrator_registry.reset(orchestrators)
        return True

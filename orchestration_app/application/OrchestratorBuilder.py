from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from domain.registry.LLMRegistry import LLMRegistry
from domain.registry.ToolRegistry import ToolRegistry
from domain.registry.OrchestratorRegistry import OrchestratorRegistry
from typing import Dict, Any, List, Union
import copy


class OrchestratorBuilder:
    def __init__(
        self,
        agentBuilderRegistry: AgentBuilderRegistry,
        llmRegistry: LLMRegistry,
        toolRegistry: ToolRegistry,
        orchestratorRegistry: OrchestratorRegistry,
    ):
        self.agentBuilderRegistry = agentBuilderRegistry
        self.llmRegistry = llmRegistry
        self.toolRegistry = toolRegistry
        self.orchestratorRegistry = orchestratorRegistry

    async def create_orchestrators_from_json(self, data: str) -> bool:
        """
        JSON 데이터를 파싱하여 오케스트레이터 리스트를 생성.

        Args:
            json_data (str): 에이전트와 오케스트레이션 정보를 포함한 JSON 문자열.

        Returns:
            List[BaseBuilder]: 생성된 에이전트 객체 리스트.

        Raises:
            ValueError: JSON 형식이 유효하지 않거나 필수 필드가 누락된 경우.
        """
        # json_data = self._load_json(data)
        json_data = data

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
                    orchestrator = await self.build_orchestrator(orchestrator_data)
                    orchestrators.append(orchestrator)
                else:
                    raise ValueError(
                        f"Invalid item format at index {idx}. Expected 'orchestrator' key."
                    )
            except Exception as e:
                raise ValueError(
                    f"Error creating orchestrator at index {idx}: {e}"
                ) from e
        await self.orchestratorRegistry.reset(orchestrators)
        return True

    async def build_orchestrator(self, orchestrator_data: Dict[str, Any]) -> Any:
        """
        JSON 데이터를 기반으로 오케스트레이터를 생성합니다.
        Args:
            orchestrator_data (dict): 오케스트레이터 정보를 포함한 JSON 데이터.
        Returns:
            Orchestrator: 생성된 오케스트레이터 객체.
        Raises:
            ValueError: JSON 형식이 유효하지 않거나 필수 필드가 누락된 경우.
        """
        try:
            if "type" not in orchestrator_data:
                raise ValueError("Orchestrator type is required.")

            builder = await self.agentBuilderRegistry.get(orchestrator_data["type"])
            if builder is None:
                raise ValueError(
                    f"Orchestrator type '{orchestrator_data['type']}' not found."
                )

            llm = await self._get_registry_item(
                orchestrator_data.get("llm"),
                self.llmRegistry,
                "LLM",
            )
            tool = await self._get_registry_item(
                orchestrator_data.get("tool"),
                self.toolRegistry,
                "Tool",
            )

            if orchestrator_data.get("llm") and not llm:
                raise ValueError(
                    f"LLM '{orchestrator_data['llm']}' not found in registry"
                )
            if orchestrator_data.get("tool") and not tool:
                raise ValueError(
                    f"Tool '{orchestrator_data['tool']}' not found in registry"
                )

            orchestrator_data = {
                k: v for k, v in orchestrator_data.items() if k not in ("llm", "tool")
            }
            orchestrator_data_copy = copy.deepcopy(orchestrator_data)

            orchestrator_data_copy["llm"] = llm if llm else None
            orchestrator_data_copy["tool"] = tool if tool else None
            await builder(**orchestrator_data_copy)
        except Exception as e:
            raise ValueError(f"Error creating orchestrator: {e}")
        return builder

    async def _get_registry_item(
        self,
        input_data: Union[str, List[str]],
        registry: Dict[str, Any],
        type: str,
    ) -> List[Any]:
        """
        str 또는 list로 주어진 입력을 받아서 레지스트리에서 객체 리스트로 변환.

        Args:
            input_data (Union[str, List[str]]): 항목 이름 또는 항목 이름 리스트.
            registry (Dict[str, Any]): 조회할 레지스트리 (llmRegistry, toolRegistry 등).
            type (str): 에러 메시지에 사용할 항목 이름 (예: 'LLM', 'Tool').

        Returns:
            List[Any]: 변환된 객체 리스트.

        Raises:
            ValueError: 레지스트리에 없는 항목이 있을 경우.
        """
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

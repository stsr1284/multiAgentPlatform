from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from domain.registry.LLMRegistry import LLMRegistry
from domain.registry.ToolRegistry import ToolRegistry
from domain.Builder.BaseBuilder import BaseBuilder
from shared.loggin_config import logger
from typing import List, Dict, Any, Union
import copy
import json


# factory 패턴이 아니기때문에 디자인패턴에 맞는 명칭을 정하기
class AgentFactory:
    def __init__(
        self,
        agentBuilderRegistry: AgentBuilderRegistry,
        llmRegistry: LLMRegistry,
        toolRegistry: ToolRegistry,
    ):
        self.agentBuilderRegistry = agentBuilderRegistry
        self.llmRegistry = llmRegistry
        self.toolRegistry = toolRegistry

    async def create_agents_from_json(self, data: str) -> List[BaseBuilder]:
        """
        JSON 데이터를 파싱하여 에이전트 리스트를 생성.

        Args:
            json_data (str): 에이전트와 오케스트레이션 정보를 포함한 JSON 문자열.

        Returns:
            List[BaseBuilder]: 생성된 에이전트 객체 리스트.

        Raises:
            ValueError: JSON 형식이 유효하지 않거나 필수 필드가 누락된 경우.
        """
        json_data = self._load_json(data)

        agents = []
        logger.info("Starting agent creation from JSON")

        if "agent_list" not in json_data:
            logger.warning(
                "No 'agent_list' found in JSON data. Returning empty agent list."
            )
            return agents
        elif "agent_list" in json_data and not isinstance(
            json_data["agent_list"], list
        ):
            raise ValueError("'agent_list' must be a list")

        json_data = json_data["agent_list"]
        for idx, item in enumerate(json_data):
            try:
                if "agent" in item:
                    agent_data = item["agent"]
                    logger.debug(f"[{idx}] Start Created agent")
                    agent = await self.build_agent(agent_data)
                    agents.append(agent)
                    logger.debug(f"[{idx}] Success Created agent: {agent.name}\n\n")
                elif "orchestration" in item:
                    orchestration_data = item["orchestration"]
                    logger.debug(f"[{idx}] Start Created orchestration")
                    agent = await self.build_orchestration(orchestration_data)
                    agents.append(agent)
                    logger.debug(
                        f"[{idx}] Success Created orchestration: {orchestration_data.get('name')}\n\n"
                    )
                else:
                    raise ValueError("Invalid item at index {idx}: {item}")
            except Exception as e:
                logger.error(f"Error creating agent/orchestration at index {idx}: {e}")
                raise

        logger.info(f"Created {len(agents)} agents")
        # test
        for agent in agents:
            logger.info(f"Agent created: {agent.name}")
        return agents

    async def build_agent(self, agent_data: Dict[str, Any]) -> Any:
        """
        단일 에이전트 데이터를 기반으로 에이전트 객체 생성.
        등록된 llm, tool를 제공하고 type에 따라 빌더를 사용하여 객체 생성.
        등록된 data 주입.

        Args:
            agent_data (Dict[str, Any]): 에이전트 정보.

        Returns:
            Any: 생성된 에이전트 빌더 객체.

        Raises:
            ValueError: 필수 필드가 누락되거나 유효하지 않은 경우.
        """
        try:
            if "type" not in agent_data:
                raise ValueError("Missing 'type' in agent data")

            builder = self.agentBuilderRegistry.get(agent_data["type"])
            if not builder:
                raise ValueError(
                    f"Agent builder not found for type: {agent_data['type']}"
                )

            llm = self._get_registry_item(
                agent_data.get("llm"), self.llmRegistry, "LLM"
            )
            tools = self._get_registry_item(
                agent_data.get("tool"), self.toolRegistry, "Tool"
            )

            if agent_data.get("llm") and not llm:
                raise ValueError(f"LLM '{agent_data['llm']}' not found in registry")
            if agent_data.get("tool") and not tools:
                raise ValueError(f"Tool '{agent_data['tool']}' not found in registry")

            agent_data_copy = {
                k: v
                for k, v in agent_data.items()
                if k not in ("llm", "tool", "agent_builder_list")
            }
            agent_data_copy = copy.deepcopy(agent_data_copy)
            if llm is not None:
                agent_data_copy["llm"] = llm
            if tools is not None:
                agent_data_copy["tool"] = tools
            if "agent_builder_list" in agent_data:
                agent_data_copy["agent_builder_list"] = agent_data["agent_builder_list"]
            await builder(**agent_data_copy)
        except Exception as e:
            logger.error(f"Error in build_agent: {e}")
            raise
        return builder

        # 에이전트 필수 필드 확인

    async def build_orchestration(self, orchestration_data: Dict[str, Any]) -> None:
        """
        오케스트레이션 데이터를 처리하여 포함된 에이전트를 생성하고 agents 리스트에 추가.

        Args:
            orchestration_data (Dict[str, Any]): 오케스트레이션 정보 (type, model, agent_list 등).
            agents (List[Any]): 생성된 에이전트를 추가할 리스트.

        Raises:
            ValueError: agent_list 항목이 유효하지 않은 경우.
        """
        try:

            if "agent_list" not in orchestration_data:
                raise ValueError(
                    f"Missing 'agent_list' in orchestration data: {orchestration_data}"
                )

            agents = []
            for item in orchestration_data["agent_list"]:
                if "agent" in item:
                    logger.info(
                        f"Processing agent in orchestration: {item['agent'].get('name')}"
                    )
                    agent = await self.build_agent(item["agent"])
                    agents.append(agent)
                elif "orchestration" in item:
                    logger.info(
                        f"Processing nested orchestration: {item['orchestration'].get('name')}"
                    )
                    agents.append(await self.build_orchestration(item["orchestration"]))

                else:
                    logger.error(f"Invalid item in agent_list: {item}")
                    raise ValueError(f"Invalid item in agent_list: {item}")

                if agents is None:
                    raise ValueError(
                        f"Agent list is empty in orchestration data: {orchestration_data}"
                    )
            orchestration_data_copy = copy.deepcopy(orchestration_data)
            orchestration_data_copy["agent_builder_list"] = agents
        except Exception as e:
            logger.error(f"Error in build_orchestration: {e}")
            raise

        return await self.build_agent(orchestration_data_copy)

    def _load_json(self, data: Union[str, dict]) -> dict:
        if isinstance(data, dict):
            return data
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def _get_registry_item(
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
            item = registry.get(item_name)
            if not item:
                raise ValueError(f"{type} '{item_name}' not found in registry")
            item_list.append(item)

        return item_list

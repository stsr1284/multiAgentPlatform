from pydantic import BaseModel
from domain.entities.RegisterAgent import RegisterAgent
from domain.interfaces.Observer import Observer

from .ToolRegistry import ToolRegistry
from .agentExecutor import AgentExecutor
from infrastructure.observers.observerManager import ObserverManager
from domain.interfaces.brokerInterface import BrokerInterface

# from .MCPManager import MCPManager



# 수정된 Broker (구성을 통한 책임 분리)
class Broker(BaseModel, BrokerInterface):

    def __init__(self, tool_list: Observer):
        self._observer_manager = ObserverManager()
        self._agent_registry = ToolRegistry(self._observer_manager)
        self._agent_executor = AgentExecutor(self._agent_registry)

        self._observer_manager.add_observer(tool_list)  # ToolListProvider를 옵저버로 등록
    
    # observer 등록 및 해제 메서드
    def add_observer(self, observer: Observer) -> None:
        self._observer_manager.add_observer(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        self._observer_manager.remove_observer(observer)

    # agent registry 메서드들
    async def register_agent(self, agent: RegisterAgent) -> None:
        await self._agent_registry.register_tool(agent)
    
    async def unregister_agent(self, agent_name: str) -> None:
        await self._agent_registry.unregister_tool(agent_name)
    
    async def execute(self, plan: dict):
        return await self._agent_executor.execute(plan)

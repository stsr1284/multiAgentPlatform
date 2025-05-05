from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.entities.BaseAgent import BaseAgent

class BrokerInterface(ABC):
    """브로커 인터페이스"""
    
    @abstractmethod
    async def execute(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """계획을 실행하는 메서드"""
        pass
    
    @abstractmethod
    async def register_agent(self, agent: BaseAgent) -> None:
        """에이전트를 등록하는 메서드"""
        pass
    
    @abstractmethod
    async def unregister_agent(self, agent_id: str) -> None:
        """에이전트를 해제하는 메서드"""
        pass
    
# from abc import ABC, abstractmethod

# # 브로커 인터페이스
# class BrokerInterface(ABC):
#     @abstractmethod
#     async def execute(self, plan: dict) -> dict:
#         pass
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.RegisterAgent import RegisterAgent

class ToolManager(ABC):
    """에이전트 관리 인터페이스"""
    
    @abstractmethod
    async def register_tool(self, agent: RegisterAgent) -> None:
        """에이전트 등록"""
        pass
    
    @abstractmethod
    async def unregister_tool(self, agent_id: str) -> None:
        """에이전트 해제"""
        pass
    
    @abstractmethod
    def get_tool(self, agent_id: str) -> Optional[RegisterAgent]:
        """에이전트 조회"""
        pass
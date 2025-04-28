import asyncio
from pydantic import Field
from shared.loggin_config import logger
from orchestration_app.domain.interfaces.AgentRepositoryInterface import (
    AgentRepositoryInterface,
)
from domain.entities.BaseAgent import BaseAgent


class AgentRepository(AgentRepositoryInterface):
    """도구 목록 레포지토리"""

    def __init__(self):
        self._agents: dict[str, BaseAgent] = {}
        self._lock = asyncio.Lock()

    async def get_agents(self) -> dict[str, BaseAgent]:
        """도구 목록 조회 (인터페이스 메서드 구현)"""
        async with self._lock:
            return self._agents

    async def set_agents(self, data: dict[str, BaseAgent]) -> None:
        """도구 목록 설정 (인터페이스 메서드 구현)"""
        async with self._lock:
            self._agents.update(data)

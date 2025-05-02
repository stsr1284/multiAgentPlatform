import asyncio
from orchestration_app.shared.loggin_config import logger
from orchestration_app.domain.interfaces.AgentRepositoryInterface import (
    AgentRepositoryInterface,
)
from orchestration_app.domain.Builder.BaseBuilder import BaseBuilder


class AgentRepository(AgentRepositoryInterface):

    def __init__(self):
        self._agents: dict[str, BaseBuilder] = {}
        self._lock = asyncio.Lock()

    async def get_agents(self) -> dict[str, BaseBuilder]:
        async with self._lock:
            return self._agents

    async def set_agents(self, data: dict[str, BaseBuilder]) -> None:
        async with self._lock:
            self._agents.update(data)

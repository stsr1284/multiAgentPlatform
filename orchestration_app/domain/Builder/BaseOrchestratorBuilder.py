from .BaseBuilder import BaseBuilder
from abc import abstractmethod


class BaseOrchestratorBuilder(BaseBuilder):

    @abstractmethod
    async def add_agent(self, agent) -> None:
        pass

    @abstractmethod
    async def reset_agent(self) -> None:
        pass

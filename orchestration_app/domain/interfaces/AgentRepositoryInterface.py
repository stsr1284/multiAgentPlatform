from abc import ABC, abstractmethod


# 도구 목록 제공자 인터페이스
class AgentRepositoryInterface(ABC):
    @abstractmethod
    async def get_agents(self):
        pass

    @abstractmethod
    async def set_agents(self, agents):
        pass

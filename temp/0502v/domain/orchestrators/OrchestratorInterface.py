from abc import ABC, abstractmethod


class OrchestratorInterface(ABC):
    @abstractmethod
    async def execute(
        session: str,
        user_id: str,
        query: str,
        agent_list: list[str],
    ):
        pass

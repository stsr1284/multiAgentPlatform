from abc import ABC, abstractmethod

class SetupAgentSystemInterface(ABC):
    @abstractmethod
    async def setup_agent_system(self):
        """
        Set up the agent system.
        """
        pass
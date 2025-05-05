from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    @abstractmethod
    async def send_request(self, message: str, history: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Send a request to the agent and return the response."""
        pass
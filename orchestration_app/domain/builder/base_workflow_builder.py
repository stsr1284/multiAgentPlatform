from abc import ABC, abstractmethod
from langgraph.graph import StateGraph


class BaseWorkflowBuilder(ABC):

    def __init__(self):
        self.type: str = self.__class__.__name__

    @abstractmethod
    async def __call__(self, **kwargs):
        pass

    @abstractmethod
    async def build() -> StateGraph:
        pass

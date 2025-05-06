from abc import ABC, abstractmethod
from domain.entyties.UserInput import UserInput
from langgraph.graph import StateGraph


class ExecutionBaseStrategy(ABC):
    @abstractmethod
    async def execute(self, graph: StateGraph, config: dict, user_input: UserInput):
        pass

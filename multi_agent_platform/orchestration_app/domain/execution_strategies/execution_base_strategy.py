from domain.entyties.user_input import UserInput
from langgraph.graph import StateGraph
from abc import ABC, abstractmethod


class ExecutionBaseStrategy(ABC):
    @abstractmethod
    async def execute(self, graph: StateGraph, config: dict, user_input: UserInput):
        pass

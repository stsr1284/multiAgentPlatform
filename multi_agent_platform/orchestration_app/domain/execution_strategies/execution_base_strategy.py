from domain.entyties.user_input import UserInput
from langgraph.graph.graph import CompiledGraph
from abc import ABC, abstractmethod


class ExecutionBaseStrategy(ABC):
    @abstractmethod
    async def execute(self, graph: CompiledGraph, config: dict, user_input: UserInput):
        pass

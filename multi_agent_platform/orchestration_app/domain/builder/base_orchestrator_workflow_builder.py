from .base_workflow_builder import BaseWorkflowBuilder
from abc import abstractmethod


class BaseOrchestratorWorkflowBuilder(BaseWorkflowBuilder):

    @abstractmethod
    async def add_agent(self, agent) -> None:
        pass

    @abstractmethod
    async def reset_agent(self) -> None:
        pass

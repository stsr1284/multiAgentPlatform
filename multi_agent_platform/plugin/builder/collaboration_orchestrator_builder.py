from domain.builder.base_orchestrator_workflow_builder import (
    BaseOrchestratorWorkflowBuilder,
)
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from langgraph_swarm import create_handoff_tool, create_swarm
from langgraph.graph.graph import CompiledGraph
from typing import Optional, Any, Callable
from langchain_core.tools import BaseTool


class CollaborationOrchestratorBuilder(BaseOrchestratorWorkflowBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.description: Optional[str] = None
        self.agent_builder_list: Optional[list[BaseWorkflowBuilder]] = []
        self.tools: Optional[list[BaseTool | Callable]] = None

    async def __call__(self, **kwargs):
        try:
            name = kwargs.get("name")
            if name is None:
                raise ValueError("name가 필요합니다")
            self.name = name

            description = kwargs.get("description")
            if description is None:
                raise ValueError("description이 필요합니다")
            self.description = description
        except Exception as e:
            raise

    async def add_agent(self, agent: BaseWorkflowBuilder) -> None:
        if not isinstance(agent, BaseWorkflowBuilder):
            raise ValueError("agent must be an instance of BaseWorkflowBuilder")
        self.agent_builder_list.append(agent)

    async def reset_agent(self) -> None:
        self.agent_builder_list = []

    async def build(self, checkpointer: Optional[Any] = None) -> CompiledGraph:
        try:

            for agent in self.agent_builder_list:
                handoff_tools = {
                    agent.name: create_handoff_tool(
                        agent_name=agent.name, description=agent.description
                    )
                    for agent in self.agent_builder_list
                }

            agent_list = []
            for agent in self.agent_builder_list:
                other_handoff_tools = [
                    handoff_tools[name] for name in handoff_tools if name != agent.name
                ]

                if hasattr(agent, "tools"):
                    agent.tools = (agent.tools or []) + other_handoff_tools
                    agent_list.append(await agent.build())
                else:
                    raise ValueError(
                        f"Agent {agent.name} does not have a tools attribute."
                    )
            self.graph = create_swarm(
                agents=agent_list,
                default_active_agent=self.agent_builder_list[0].name,
            )
            compiled_graph = self.graph.compile(
                name=self.name, checkpointer=checkpointer
            )
        except Exception as e:
            raise e
        return compiled_graph


async def register(registry):
    try:
        await registry.register(CollaborationOrchestratorBuilder)
    except Exception as e:
        raise e

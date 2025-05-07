from domain.execution_strategies.execution_base_strategy import ExecutionBaseStrategy
from domain.registry.orchestrator_registry import OrchestratorRegistry
from langgraph.checkpoint.base import BaseCheckpointSaver
from domain.entyties.user_input import OrchestrationInput
from domain.registry.agent_registry import AgentRegistry
from domain.registry.graph_registry import GraphRegistry
from langgraph.graph import StateGraph


class OrchestrationService:
    def __init__(
        self,
        agent_registry: AgentRegistry,
        orchestrator_registry: OrchestratorRegistry,
        graph_registry: GraphRegistry,
    ):
        self.agent_registry = agent_registry
        self.orchestrator_registry = orchestrator_registry
        self.graph_registry = graph_registry

    async def build_graph_and_config(
        self, orchestration_input: OrchestrationInput, checkpointer: BaseCheckpointSaver
    ) -> tuple[StateGraph, dict] | None:
        builders = []
        for name in orchestration_input.agent_list:
            builder = await self.agent_registry.get(name)
            if builder is None:
                raise ValueError(f"Agent {name} not found in registry.")
            builders.append(builder)
        if not builders:
            raise ValueError("No valid agents found in the user input agent list.")

        orchestrator = await self.orchestrator_registry.get(
            orchestration_input.orchestrator_type
        )
        if orchestrator is None:
            raise ValueError(
                f"Orchestrator {orchestration_input.orchestrator_type} not found in registry."
            )
        await orchestrator.reset_agent()
        [await orchestrator.add_agent(agent) for agent in builders]
        graph = await orchestrator.build(checkpointer)
        config = {
            "configurable": {
                "thread_id": orchestration_input.thread_id,
            }
        }
        return graph, config

    async def run(
        self,
        execution_strategy: ExecutionBaseStrategy,
        orchestration_input: OrchestrationInput,
        checkpointer: BaseCheckpointSaver,
    ):
        try:
            previous_graph = await self.graph_registry.get_all()
            if orchestration_input.thread_id in previous_graph:
                await self.graph_registry.unregister(orchestration_input.thread_id)
            graph_config = await self.build_graph_and_config(
                orchestration_input, checkpointer
            )
            if graph_config is None:
                raise ValueError("Graph and config are None.")
            graph, config = graph_config
            return await execution_strategy.execute(graph, config, orchestration_input)
        except Exception as e:
            raise ValueError(f"Error in orchestration service: {e}") from e

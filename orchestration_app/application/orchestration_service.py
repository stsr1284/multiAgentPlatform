from domain.execution_strategies.execution_base_strategy import ExecutionBaseStrategy
from domain.registry.OrchestratorRegistry import OrchestratorRegistry
from langgraph.checkpoint.base import BaseCheckpointSaver
from domain.registry.AgentRegistry import AgentRegistry
from domain.registry.GraphRegistry import GraphRegistry
from domain.entyties.UserInput import OrchestrationInput
from shared.loggin_config import logger
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
                logger.error("Graph and config are None.")
                return None
            graph, config = graph_config
            return await execution_strategy.execute(graph, config, orchestration_input)
        except Exception as e:
            logger.error(f"Error in orchestration service: {e}")
            return None

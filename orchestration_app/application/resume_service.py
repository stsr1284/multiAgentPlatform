from domain.execution_strategies.execution_base_strategy import ExecutionBaseStrategy
from domain.entyties.InterruptThreadGraph import InterruptThreadGraph
from domain.registry.GraphRegistry import GraphRegistry
from domain.entyties.UserInput import UserInput


class ResumeService:
    def __init__(self, graph_registry: GraphRegistry):
        self.graph_registry = graph_registry

    async def run(
        self, execution_strategy: ExecutionBaseStrategy, user_input: UserInput
    ):
        try:
            item: InterruptThreadGraph = await self.graph_registry.get(
                user_input.thread_id
            )
            graph = item.graph
            config = {
                "configurable": {
                    "thread_id": user_input.thread_id,
                }
            }
            return await execution_strategy.execute(
                graph=graph,
                config=config,
                user_input=user_input,
            )
        except Exception as e:
            raise ValueError(f"Error in ResumeService: {e}")

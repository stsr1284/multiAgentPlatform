from domain.entyties.interrupt_thread_graph import InterruptThreadGraph
from .execution_base_strategy import ExecutionBaseStrategy
from domain.registry.graph_registry import GraphRegistry
from domain.entyties.user_input import UserInput
from langgraph.graph import StateGraph
import json


class OrchestrationAStreamStrategy(ExecutionBaseStrategy):
    def __init__(self, graph_registry: GraphRegistry):
        self.graph_registry = graph_registry

    async def execute(self, graph: StateGraph, config: dict, user_input: UserInput):
        initial_input = {"messages": [{"role": "user", "content": user_input.query}]}

        async def event_stream():
            async for event in graph.astream(
                initial_input, config, stream_mode="updates"
            ):
                for key, value in event.items():
                    if key == "__interrupt__":
                        if value[0].resumable:
                            await self.graph_registry.register(
                                InterruptThreadGraph(
                                    thread_id=user_input.thread_id, graph=graph
                                )
                            )
                            yield json.dumps(
                                {
                                    "type": "interrupt",
                                    "message": value[0].value,
                                }
                            ) + "\n"
                        else:
                            raise ValueError("Thread is not resumable")
                    else:
                        yield json.dumps(
                            {
                                "type": "message",
                                "message": value["messages"][-1].content,
                            }
                        ) + "\n"

        return event_stream()

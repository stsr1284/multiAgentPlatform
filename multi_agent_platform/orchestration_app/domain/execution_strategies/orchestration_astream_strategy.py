from domain.entyties.interrupt_thread_graph import InterruptThreadGraph
from .execution_base_strategy import ExecutionBaseStrategy
from domain.registry.graph_registry import GraphRegistry
from domain.entyties.user_input import UserInput
from langgraph.graph.graph import CompiledGraph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import json


class OrchestrationAStreamStrategy(ExecutionBaseStrategy):
    def __init__(self, graph_registry: GraphRegistry):
        self.graph_registry = graph_registry

    async def execute(self, graph: CompiledGraph, config: dict, user_input: UserInput):
        initial_input = {"messages": [{"role": "user", "content": user_input.query}]}

        async def event_stream():
            try:
                async for event in graph.astream(
                    initial_input, config, stream_mode="values", subgraphs=True
                ):
                    agent: str = None
                    agent_type = event[0]
                    if len(agent_type):
                        agent = agent_type[-1].split(":")[0]
                    if "messages" in event[1]:
                        if isinstance(event[1]["messages"][-1], HumanMessage):
                            if agent is None:
                                continue
                            else:
                                yield json.dumps(
                                    {
                                        "type": "message",
                                        "agent": agent,
                                        "tool_name": None,
                                        "message": event[1]["messages"][-1].content,
                                    }
                                ) + "\n"

                        elif isinstance(event[1]["messages"][-1], AIMessage):
                            if agent is None:
                                yield json.dumps(
                                    {
                                        "type": "end",
                                        "agent": None,
                                        "tool_name": None,
                                        "message": event[1]["messages"][-1].content,
                                    }
                                ) + "\n"
                            if event[1]["messages"][-1].tool_calls:
                                yield json.dumps(
                                    {
                                        "type": "tool_calls",
                                        "agent": agent,
                                        "tool_name": None,
                                        "message": event[1]["messages"][-1].tool_calls[
                                            0
                                        ]["name"],
                                    }
                                ) + "\n"
                            elif not event[1]["messages"][-1].tool_calls:
                                yield json.dumps(
                                    {
                                        "type": "message",
                                        "agent": agent,
                                        "tool_name": None,
                                        "message": event[1]["messages"][-1].content,
                                    }
                                ) + "\n"
                        elif isinstance(event[1]["messages"][-1], ToolMessage):
                            yield json.dumps(
                                {
                                    "type": "tool",
                                    "agent": None,
                                    "tool_name": event[1]["messages"][-1].name,
                                    "message": event[1]["messages"][-1].content,
                                }
                            ) + "\n"

                    else:
                        if event[1]["__interrupt__"][0].resumable and agent is not None:
                            await self.graph_registry.register(
                                InterruptThreadGraph(
                                    thread_id=user_input.thread_id, graph=graph
                                )
                            )
                            yield json.dumps(
                                {
                                    "type": "interrupt",
                                    "agent": None,
                                    "tool_name": None,
                                    "message": event[1]["__interrupt__"][0].value,
                                }
                            ) + "\n"
            except Exception as e:
                yield json.dumps(
                    {
                        "type": "error",
                        "agent": None,
                        "tool_name": None,
                        "message": str(e),
                    }
                ) + "\n"

        return event_stream()

from domain.execution_strategies.execution_base_strategy import ExecutionBaseStrategy
from domain.entyties.user_input import UserInput
from shared.loggin_config import logger
from langgraph.graph import StateGraph
from langgraph.types import Command
import json


class ResumeAStreamStrategy(ExecutionBaseStrategy):
    def __init__(self, graph_registry):
        self.graph_registry = graph_registry

    async def execute(self, graph: StateGraph, config: dict, user_input: UserInput):
        async def event_stream():

            try:
                async for event in graph.astream(
                    Command(resume=user_input.query),
                    config,
                    stream_mode="updates",
                ):
                    for key, value in event.items():
                        if key == "__interrupt__":
                            if value[0].resumable:
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
            except Exception as e:
                logger.error(f"Error in event stream: {e}")

        return event_stream()

from domain.entyties.interrupt_thread_graph import InterruptThreadGraph
from .execution_base_strategy import ExecutionBaseStrategy
from domain.registry.graph_registry import GraphRegistry
from domain.entyties.user_input import UserInput
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import json


class OrchestrationAStreamStrategy(ExecutionBaseStrategy):
    def __init__(self, graph_registry: GraphRegistry):
        self.graph_registry = graph_registry

    async def execute(self, graph: StateGraph, config: dict, user_input: UserInput):
        initial_input = {"messages": [{"role": "user", "content": user_input.query}]}

        async def event_stream():
            async for event in graph.astream(
                initial_input, config, stream_mode="values", subgraphs=True
            ):
                print("------------------------------------")
                print(type(event))
                print("1")
                agent: str = None
                agent_type = event[0]
                if len(agent_type):  # 없는 경우 1. 마지막 대답일 때, 2. toolMessage일때
                    agent = agent_type[0].split(":")[0]
                    print("dsfsdfsdf", agent_type[0])
                print("agent: ", agent_type)
                print("agent: ", type(agent_type))
                print("2")
                print("event:", event)
                # print("event:", event)
                if "messages" in event[1]:
                    # 현재 분류 다 했으니깐 프론트는 agent 받은거에 빛내고, meesage 받은거나 tool_call이면 표시하기
                    if isinstance(event[1]["messages"][-1], HumanMessage):
                        print("Humman Message!!")
                        print("message:", event[1]["messages"][-1])
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

                    # AIMEssage인데 event[0]이 없으면 최동 대답
                    elif isinstance(event[1]["messages"][-1], AIMessage):
                        print("AI Message!!")
                        print("message:", event[1]["messages"][-1])
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
                            print("tool_calls:", event[1]["messages"][-1].tool_calls)
                            yield json.dumps(
                                {
                                    "type": "tool_calls",
                                    "agent": agent,
                                    "tool_name": None,
                                    "message": event[1]["messages"][-1].tool_calls[0][
                                        "name"
                                    ],
                                }
                            ) + "\n"
                        elif not event[1]["messages"][-1].tool_calls:
                            print("tools_calls 없음!")
                            yield json.dumps(
                                {
                                    "type": "message",
                                    "agent": agent,
                                    "tool_name": None,
                                    "message": event[1]["messages"][-1].content,
                                }
                            ) + "\n"
                    elif isinstance(event[1]["messages"][-1], ToolMessage):
                        print("Tool Message!!")
                        print("message:", event[1]["messages"][-1])
                        yield json.dumps(
                            {
                                "type": "tool",
                                "agent": None,
                                "tool_name": event[1]["messages"][-1].name,
                                "message": event[1]["messages"][-1].content,
                            }
                        ) + "\n"

                        # if event[1]["messages"][-1].tool_calls:
                        #     print("message:", event[1]["messages"][-1].content)
                else:
                    print("인터럽드 발생!!!")
                    print("message:", event[1]["__interrupt__"][0].value)
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
                print("------------------------------------")
                # for chunk in event:

                #     print("chunk:", chunk)
                # for key, value in event.items():
                #     print("------------------------------------")
                #     print("key:", key)  # test
                #     print("value:", value)  # test
                #     print("------------------------------------")
                #     if key == "__interrupt__":
                #         if value[0].resumable:
                #             await self.graph_registry.register(
                #                 InterruptThreadGraph(
                #                     thread_id=user_input.thread_id, graph=graph
                #                 )
                #             )
                #             yield json.dumps(
                #                 {
                #                     "type": "interrupt",
                #                     "message": value[0].value,
                #                 }
                #             ) + "\n"
                #         else:
                #             raise ValueError("Thread is not resumable")
                #     else:
                #         yield json.dumps(
                #             {
                #                 "type": "message",
                #                 "message": value["messages"][-1].content,
                #             }
                #         ) + "\n"

        return event_stream()

from domain.registry.OrchestratorRegistry import OrchestratorRegistry
from domain.registry.AgentRegistry import AgentRegistry
from domain.entyties.UserInput import UserInput
from shared.loggin_config import logger
from langgraph.checkpoint.base import BaseCheckpointSaver

# test
from IPython.display import Image, display
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.types import Command
from domain.entyties.InterruptThreadGraph import InterruptThreadGraph  # test
from domain.registry.GraphRegistry import GraphRegistry  # test


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

    # orchestration받기 userInput받기, orchestariont에 userInput넣으면 builde가 되고
    # orchestration 리턴을 run한다
    async def run(self, user_input: UserInput, checkpointer: BaseCheckpointSaver):
        builders = []
        for name in user_input.agent_list:
            try:
                builder = await self.agent_registry.get(name)
                print("builder", builder)
                if builder is None:
                    raise ValueError(f"Agent {name} not found in registry.")
                # builders.append(builder)
                builders.append(builder)
            except Exception as e:
                logger.error(f"Error getting agent {name}: {e}")
                continue
        if not builders:
            logger.error("No valid agents found.")
            return None

        orchestrator = await self.orchestrator_registry.get(
            user_input.orchestrator_type
        )
        if orchestrator is None:
            logger.error(
                f"Orchestrator {user_input.orchestrator_type} not found in registry."
            )
            return None

        for agent in builders:
            print("orchestrationService")
            print(agent.name)
            print(agent, "\n")
        await orchestrator.reset_agent()  # 필수
        [await orchestrator.add_agent(agent) for agent in builders]  # 필수
        # orchestrator.agent_list = builders
        # checkpointer build()에 넣어주기

        graph = await orchestrator.build(checkpointer)
        print("시각화")
        print(graph.get_graph().draw_mermaid())
        print("---------------")
        config = {
            "configurable": {"user_id": user_input.id, "thread_id": user_input.session}
        }
        config2 = {
            "configurable": {"user_id": user_input.id, "thread_id": user_input.session}
        }
        try:
            # result = await graph.ainvoke(
            #     {
            #         "messages": [
            #             {
            #                 "role": "user",
            #                 "content": user_input.query,
            #             }
            #         ]
            #     },
            #     config,
            # )
            initial_input = {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input.query,
                    }
                ]
            }

            #  {'__interrupt__': (Interrupt(value='안뇽 나는 interrupt를 호출할고얌!!', resumable=True, ns=['math_expert:204c48c4-22e8-61c7-5d50-1ba5d622edcc', 'tools:3bdf5b21-a9d9-e55f-b03f-b869002ac0ea']),)}
            async for event in graph.astream(
                initial_input, config, stream_mode="updates"
            ):
                print("----------------")
                for key, value in event.items():
                    if key == "__interrupt__":
                        print("interrupt 발생")
                        print(value)
                        await self.graph_registry.register(
                            InterruptThreadGraph(
                                thread_id=user_input.session,
                                graph=graph,
                            )
                        )
                    else:
                        print("messages 발생")
                        print(key, ": ", value["messages"][-1].content)
                print("-------------------")
            # db error 밑에 있는거
            # 2025-05-05 16:18:32,530 - psycopg.pool - WARNING - discarding closed connection: <psycopg.AsyncConnection [BAD] at 0x10aa9bb50>
            # 2025-05-05 16:18:32,573 - shared.loggin_config - ERROR - Error building orchestrator: {:shutdown, :db_termination}
            print("재개해볼게!")
            # result2 = await graph.ainvoke(
            #     Command(resume="동하깅동하깅!!!!!"),
            #     config2,
            # )
            # for key, value in result2.items():
            #     if key == "messages":
            #         for message in value:
            #             print(f"{message.pretty_print()}\n")

        except Exception as e:
            logger.error(f"Error building orchestrator: {e}")
            return None
        return "god"

        # build = create_supervisor(agents=builders, model=llmModel)
        # graph = build.compile(name="supervisor")
        # result = graph.invoke(
        #     {
        #         "messages": [
        #             {
        #                 "role": "user",
        #                 "content": user_input.query,
        #             }
        #         ]
        #     },
        # )

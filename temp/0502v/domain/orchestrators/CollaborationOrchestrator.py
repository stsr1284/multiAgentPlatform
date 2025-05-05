from .OrchestratorInterface import OrchestratorInterface
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent  # test
from langchain_core.language_models.chat_models import BaseChatModel
from orchestration_app.domain.entities.AgentDefinition import AgentDefinition
from langgraph_swarm import create_handoff_tool, create_swarm


# agent_list: list[CompiledGraph | Pregel],
class CollaborationOrchestrator(OrchestratorInterface):
    def __init__(
        self,
        agent_recipe_list: list[AgentDefinition],
        output_mode: str = "full_history",
    ):

        # self.compile_agent_list = [agent.compile() for agent in agent_list]
        try:
            print("what happened")
            for agent in agent_recipe_list:  # test
                print(agent.name, " ", agent.description)
            handoff_tools = {
                agent.name: create_handoff_tool(
                    agent_name=agent.name, description=agent.description
                )
                for agent in agent_recipe_list
            }

            print("what happened")
            # 에이전트 리스트 생성
            agent_list = []
            for agent in agent_recipe_list:
                # 자신을 제외한 다른 에이전트의 handoff 도구
                other_handoff_tools = [
                    handoff_tools[name] for name in handoff_tools if name != agent.name
                ]

                # create_react_agent 호출
                [
                    print("나 외에 name: ", name)
                    for name in handoff_tools
                    if name != agent.name
                ]
                print("name: ", agent.name)
                agent_list.append(
                    create_react_agent(
                        model=agent.llm,
                        tools=(agent.tools or []) + other_handoff_tools,
                        name=agent.name,
                        prompt=agent.prompt,
                        config_schema=agent.config,
                    )
                )
            print("start agent: ", agent_recipe_list[0].name)
            workflow = create_swarm(
                agents=agent_list,
                default_active_agent=agent_recipe_list[0].name,
            )
            print("collaboration agent 1")
            self.graph = workflow.compile()
        except Exception as e:
            print("ManagementOrchestrator init error:", e)
            raise e

    def execute(self):
        """계획을 실행하는 메서드"""
        return self.graph

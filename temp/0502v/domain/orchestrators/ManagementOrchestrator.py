from .OrchestratorInterface import OrchestratorInterface
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent  # test
from langchain_core.language_models.chat_models import BaseChatModel
from orchestration_app.domain.entities.AgentDefinition import AgentDefinition


# agent_list: list[CompiledGraph | Pregel],
class ManagementOrchestrator(OrchestratorInterface):
    def __init__(
        self,
        model: BaseChatModel,
        agent_recipe_list: list[AgentDefinition],
        output_mode: str = "full_history",
        prompt: str = None,
    ):

        # self.compile_agent_list = [agent.compile() for agent in agent_list]
        try:
            agent_list = []
            for agent in agent_recipe_list:
                agent_list.append(
                    create_react_agent(
                        model=agent.llm,
                        tools=agent.tools,
                        name=agent.name,
                        prompt=agent.prompt,
                        config_schema=agent.config,
                    )
                )
            members = [agent.name for agent in agent_list]
            options = ["FINISH"] + members
            # 기본 프롬프트 템플릿
            default_prompt = (
                "You are a supervisor tasked with managing a conversation between the"
                f" following workers: {members}. Given the following user request,"
                " respond with the worker to act next. Each worker will perform a"
                " task and respond with their results and status. When finished,"
            )

            # 프롬프트 템플릿이 제공되면 이를 사용, 아니면 기본 프롬프트 사용
            system_prompt = prompt.format(members=members) if prompt else default_prompt

            graph = create_supervisor(
                model=model,
                agents=agent_list,
                output_mode=output_mode,
                prompt=system_prompt,
            )
            self.graph = graph.compile()
        except Exception as e:
            print("ManagementOrchestrator init error:", e)
            raise e

    def execute(self):
        """계획을 실행하는 메서드"""
        return self.graph

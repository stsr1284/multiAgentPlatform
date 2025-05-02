from langchain_core.language_models.chat_models import BaseChatModel
from shared.loggin_config import logger
from langgraph_supervisor import create_supervisor
from typing import Optional, Callable, Any
from langchain_core.tools import BaseTool

from domain.Builder.BaseBuilder import BaseBuilder

# 입력 예시
# self.llms: Optional[List[BaseChatModel]] = None
# self.tools: Optional[list[BaseTool | Callable]] = None
# self.prompts: Optional[list[str]] = None
# self.agent_builder_list = Optional[list[BaseBuilder]] = None


# 이거 llm, prompt, tool 받도록 해야됨
class SupervisorAgentBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.tools: Optional[list[BaseTool | Callable]] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None
        self.config: Optional[dict[str, Any]] = None
        self.agent_builder_list: Optional[list[BaseBuilder]] = None

    async def __call__(self, **kwargs):
        try:
            print(
                "-----------------SupervisorAgentBuilder __call__---------------------"
            )
            name = kwargs.get("name")
            if name is None:
                raise ValueError("name가 필요합니다")
            self.name = name
            llms = kwargs.get("llm")
            if llms is None:
                raise ValueError("llms가 필요합니다.")
            self.llm = llms[0]

            tools = kwargs.get("tool")
            if tools:
                self.tools = tools

            prompts = kwargs.get("prompt")
            if prompts:
                self.prompt = prompts

            agent_builder_list = kwargs.get("agent_builder_list")
            if agent_builder_list is None:
                raise ValueError("agent_builder_list가 필요합니다.")
            self.agent_builder_list = agent_builder_list
            agent_list = []
            for agent in self.agent_builder_list:  # test
                print(
                    f"type: {agent.type}, name: {agent.name}, llm: {agent.llm.model_name}"
                )  # test
                agent_list.append(await agent.build())
            self.agent_list = agent_list
            members = [agent.name for agent in self.agent_builder_list]
            options = ["FINISH"] + members
            default_prompt = (
                "You are a supervisor tasked with managing a conversation between the"
                f" following workers: {options}. Given the following user request,"
                " respond with the worker to act next. Each worker will perform a"
                " task and respond with their results and status. When finished,"
            )

            system_prompt = (
                self.prompt.format(members=members) if self.prompt else default_prompt
            )
            self.prompt = system_prompt

        except Exception as e:
            logger.error(f"SupervisorAgentBuilder Error: {e}")
            raise

    async def build(self):
        try:
            self.graph = create_supervisor(
                model=self.llm,
                prompt=self.prompt,
                agents=self.agent_list,
                tools=self.tools,
            )
            compiled_graph = self.graph.compile(name=self.name)
        except Exception as e:
            logger.error(f"error: {e}")
            raise
        return compiled_graph


async def register(registry):
    try:
        await registry.register(SupervisorAgentBuilder)
    except Exception as e:
        raise


# class SupervisorAgentBuilder(BaseOrchestrationBuilder):
#     async def build(self, input: SupervisorOrchestrationBuilderInput):
#         try:
#             agent_list = []
#             for agent in input.agentProfiles:
#                 if agent.get("is_custome", True):
#                     if "type" not in agent:
#                         raise ValueError("Agent type is required.")
#                     builder = input.agentBuilderRegistry.get(agent["type"])
#                     if not builder:
#                         raise ValueError(
#                             f"Builder not found for agent type: {agent['type']}"
#                         )
#                     agent_list.append(builder(**agent))

#                 else:
#                     if isinstance(agent, dict):
#                         agent = AgentDefinition(**agent)
#                     if not isinstance(agent, AgentDefinition):
#                         raise ValueError(
#                             "Agent must be a dictionary or AgentDefinition."
#                         )
#                     builder = input.agentBuilderRegistry.get(agent.type)
#                     if not builder:
#                         raise ValueError(
#                             f"Builder not found for agent type: {agent.type}"
#                         )
#                     llm = input.llmRegistry.get(agent.llm)
#                     if not llm:
#                         raise ValueError(f"LLM not found for agent: {agent.llm}")
#                     tools = [input.toolRegistry.get(tool) for tool in agent.tools]
#                     if not tools:
#                         raise ValueError(f"Tools not found for agent: {agent.tools}")
#                     agent_list.append(builder(agent))

#                     members = [agent.name for agent in agent_list]
#                     options = ["FINISH"] + members
#                     # 기본 프롬프트 템플릿
#                     default_prompt = (
#                         "You are a supervisor tasked with managing a conversation between the"
#                         f" following workers: {options}. Given the following user request,"
#                         " respond with the worker to act next. Each worker will perform a"
#                         " task and respond with their results and status. When finished,"
#                     )

#                     # 프롬프트 템플릿이 제공되면 이를 사용, 아니면 기본 프롬프트 사용
#                     system_prompt = (
#                         input.prompt.format(members=members)
#                         if input.prompt
#                         else default_prompt
#                     )
#                     graph = create_supervisor()

#         except Exception as e:
#             logger.error(f"error: {e}")
#             raise

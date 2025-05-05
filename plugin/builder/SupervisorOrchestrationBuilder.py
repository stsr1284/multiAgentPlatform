from langchain_core.language_models.chat_models import BaseChatModel
from langgraph_supervisor import create_supervisor
from langgraph.graph import StateGraph

from domain.builder.BaseBuilder import BaseBuilder
from domain.builder.BaseOrchestratorBuilder import BaseOrchestratorBuilder
from typing import Optional, Callable, Any
from langchain_core.tools import BaseTool
from shared.loggin_config import logger


class SupervisorOrchestrationBuilder(BaseOrchestratorBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.tools: Optional[list[BaseTool | Callable]] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None
        self.config: Optional[dict[str, Any]] = None
        self.agent_builder_list: Optional[list[BaseBuilder]] = []
        self.agent_list: Optional[list[StateGraph]] = []

    async def __call__(self, **kwargs):
        try:
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

        except Exception as e:
            logger.error(f"SupervisorAgentBuilder Error: {e}")
            raise

    async def add_agent(self, agent: BaseBuilder) -> None:
        """Add an agent to the agent list."""
        print(f"{self.name} add_agent:{agent.name}")
        if not isinstance(agent, BaseBuilder):
            raise ValueError("agent must be an instance of BaseBuilder")
        self.agent_builder_list.append(agent)

    async def reset_agent(self) -> None:
        """Reset the agent list."""
        print(f"{self.name} reset_agent")
        self.agent_builder_list = []

    async def build(self, checkpointer: Optional[Any] = None) -> StateGraph:
        try:
            print("1")
            print("prompt:", self.prompt)
            system_prompt = self.prompt
            if self.prompt is None:
                members = []
                members = [agent.name for agent in self.agent_builder_list]
                options = ["FINISH"] + members
                default_prompt = (
                    "You are a supervisor tasked with managing a conversation between the"
                    f" following workers: {options}. Given the following user request,"
                    " respond with the worker to act next. Each worker will perform a"
                    " task and respond with their results and status. When finished,"
                )

                system_prompt = default_prompt.format(options=options)

            agent_list = []
            for agent in self.agent_builder_list:
                print("agent name:", agent.name)
                print("agent:", agent, "\n")
                agent_list.append(await agent.build())
                # 중첩 방지를 위해서 매번 새로 builder하여 저장하도록 변경
                # self.agent_list = agent_list

            self.graph = create_supervisor(
                model=self.llm,
                prompt=system_prompt,
                agents=agent_list,
                output_mode="full_history",  # test
                add_handoff_back_messages=True,  # test
                tools=self.tools,
            )
            print(f"{self.name}: 자 컴파일 드갑니다잉")
            compiled_graph = self.graph.compile(
                name=self.name, checkpointer=checkpointer
            )
        except Exception as e:
            logger.error(f"error: {e}")
            raise
        return compiled_graph


async def register(registry):
    try:
        await registry.register(SupervisorOrchestrationBuilder)
    except Exception as e:
        raise


# class SupervisorOrchestrationBuilder(BaseBuilder):
#     def __init__(self):
#         super().__init__()
#         self.name: Optional[str] = None
#         self.llm: Optional[BaseChatModel] = None
#         self.tools: Optional[list[BaseTool | Callable]] = None
#         self.prompt: Optional[str] = None
#         self.description: Optional[str] = None
#         self.config: Optional[dict[str, Any]] = None
#         self.agent_builder_list: Optional[list[BaseBuilder]] = None

#     async def __call__(self, **kwargs):
#         try:
#             name = kwargs.get("name")
#             if name is None:
#                 raise ValueError("name가 필요합니다")
#             self.name = name
#             llms = kwargs.get("llm")
#             if llms is None:
#                 raise ValueError("llms가 필요합니다.")
#             self.llm = llms[0]

#             tools = kwargs.get("tool")
#             if tools:
#                 self.tools = tools

#             prompts = kwargs.get("prompt")
#             if prompts:
#                 self.prompt = prompts

#             agent_builder_list = []
#             if kwargs.get("agent_builder_list"):
#                 agent_builder_list = kwargs.get("agent_builder_list")
#             # agent_builder_list = kwargs.get("agent_builder_list")
#             # if agent_builder_list is None:
#             #     raise ValueError("agent_builder_list가 필요합니다.")
#             self.agent_builder_list = agent_builder_list
#             agent_list = []
#             for agent in self.agent_builder_list:
#                 agent_list.append(await agent.build())
#             self.agent_list = agent_list
#             members = [agent.name for agent in self.agent_builder_list]
#             options = ["FINISH"] + members
#             default_prompt = (
#                 "You are a supervisor tasked with managing a conversation between the"
#                 f" following workers: {options}. Given the following user request,"
#                 " respond with the worker to act next. Each worker will perform a"
#                 " task and respond with their results and status. When finished,"
#             )

#             system_prompt = (
#                 self.prompt.format(members=members) if self.prompt else default_prompt
#             )
#             self.prompt = system_prompt

#         except Exception as e:
#             logger.error(f"SupervisorAgentBuilder Error: {e}")
#             raise

#     async def build(self):
#         try:
#             print("prompt:", self.prompt)
#             self.graph = create_supervisor(
#                 model=self.llm,
#                 prompt=self.prompt,
#                 agents=self.agent_list,
#                 tools=self.tools,
#             )
#             compiled_graph = self.graph.compile(name=self.name)
#         except Exception as e:
#             logger.error(f"error: {e}")
#             raise
#         return compiled_graph


# async def register(registry):
#     try:
#         await registry.register(SupervisorOrchestrationBuilder)
#     except Exception as e:
#         raise
# class SupervisorOrchestrationBuilder(BaseBuilder):
#     def __init__(self):
#         super().__init__()
#         self.name: Optional[str] = None
#         self.llm: Optional[BaseChatModel] = None
#         self.tools: Optional[list[BaseTool | Callable]] = None
#         self.prompt: Optional[str] = None
#         self.description: Optional[str] = None
#         self.config: Optional[dict[str, Any]] = None
#         self.agent_builder_list: Optional[list[BaseBuilder]] = None

#     async def __call__(self, **kwargs):
#         try:
#             name = kwargs.get("name")
#             if name is None:
#                 raise ValueError("name가 필요합니다")
#             self.name = name
#             llms = kwargs.get("llm")
#             if llms is None:
#                 raise ValueError("llms가 필요합니다.")
#             self.llm = llms[0]

#             tools = kwargs.get("tool")
#             if tools:
#                 self.tools = tools

#             prompts = kwargs.get("prompt")
#             if prompts:
#                 self.prompt = prompts

#             agent_builder_list = []
#             if kwargs.get("agent_builder_list"):
#                 agent_builder_list = kwargs.get("agent_builder_list")
#             # agent_builder_list = kwargs.get("agent_builder_list")
#             # if agent_builder_list is None:
#             #     raise ValueError("agent_builder_list가 필요합니다.")
#             self.agent_builder_list = agent_builder_list
#             agent_list = []
#             for agent in self.agent_builder_list:
#                 agent_list.append(await agent.build())
#             self.agent_list = agent_list
#             members = [agent.name for agent in self.agent_builder_list]
#             options = ["FINISH"] + members
#             default_prompt = (
#                 "You are a supervisor tasked with managing a conversation between the"
#                 f" following workers: {options}. Given the following user request,"
#                 " respond with the worker to act next. Each worker will perform a"
#                 " task and respond with their results and status. When finished,"
#             )

#             system_prompt = (
#                 self.prompt.format(members=members) if self.prompt else default_prompt
#             )
#             self.prompt = system_prompt

#         except Exception as e:
#             logger.error(f"SupervisorAgentBuilder Error: {e}")
#             raise

#     async def build(self):
#         try:
#             print("prompt:", self.prompt)
#             self.graph = create_supervisor(
#                 model=self.llm,
#                 prompt=self.prompt,
#                 agents=self.agent_list,
#                 tools=self.tools,
#             )
#             compiled_graph = self.graph.compile(name=self.name)
#         except Exception as e:
#             logger.error(f"error: {e}")
#             raise
#         return compiled_graph


# async def register(registry):
#     try:
#         await registry.register(SupervisorOrchestrationBuilder)
#     except Exception as e:
#         raise

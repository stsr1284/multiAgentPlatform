from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from typing import Optional, Callable, Any
from langchain_core.tools import BaseTool
from domain.Builder.BaseBuilder import BaseBuilder
from shared.loggin_config import logger


class ReactAgentBuilder(BaseBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.tools: Optional[list[BaseTool | Callable]] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None
        self.config: Optional[dict[str, Any]] = None

    async def __call__(self, **kwargs):
        try:
            logger.debug("ReactAgentBuilder __call__")
            name = kwargs.get("name")
            if name is None:
                raise ValueError("name가 필요합니다")
            self.name = name
            llms = kwargs.get("llm")
            if llms is None:
                raise ValueError("llm가 필요합니다.")
            self.llm = llms[0]

            tools = kwargs.get("tool")
            if tools:
                self.tools = tools

            prompts = kwargs.get("prompt")
            if prompts:
                self.prompt = prompts

            description = kwargs.get("description")
            if description:
                self.description = description

            config = kwargs.get("config")
            if config:
                self.config = config

            logger.info(
                f"[Agent Info] type: {self.type}, name: {self.name}, llm: {self.llm.model_name}"
            )
        except Exception as e:
            raise e

    async def build(self):
        try:
            graph = create_react_agent(
                model=self.llm,
                tools=self.tools,
                name=self.name,
                prompt=self.prompt,
                config_schema=self.config,
            )
        except Exception as e:
            raise e
        return graph


async def register_builder(registry):
    try:
        await registry.register(ReactAgentBuilder)
    except Exception as e:
        raise e


# class ReactAgentBuilder(BaseBuilder):
#     async def __call__(self, **kwargs):
#         profile = AgentDefinition(**kwargs)
#         self.name = profile


#     async def build(self, profile):
#         graph = create_react_agent(
#             model=profile.llm,
#             tools=profile.tools,
#             name=profile.name,
#             prompt=profile.prompt,
#             config_schema=profile.config,
#         )
#         return graph


# 파서
# 1. 에이전트 인수를 받아서 .compile()만 하면 되도록 -> 객체 내부에서 파싱하여 필요한 인수들 가지고있음
# 	1. agent? -> type에 맞는 빌더를 agentBuilderRegistry에서 가져옴
# 	2. 내부 인수들 call에 넣음 -> 객체 변수에 담아서 build()만 하면 되도록 만들어두기
# 2. 오케스트레이션: 에이전트들은 .compile()만 하면 되고 협업인 경우 tools에 hand-off만 추가하면 되도록
# 	- 재귀적으로 들어갈때 agent는 .compile 전 단계 까지 만들고 list 객체에 담고 탈출문에서 수퍼바이저 빌더에 넣어서 llm, tools, agent_list에 담기만 함, 이후 compile에서 조합해서 compile하기
# 	- orchestration? -> 재귀문에 들어감
# 	- agent? 빌더 불러서 객체 만들고 agent list에 담기
# 	- orchestration? 재귀 진입, 탈출 하면 agent list에 담기
# 	- 탈출문에서 supervisor 빌더에 인자들 다 넣기 -> 본인 인자 + agent_list

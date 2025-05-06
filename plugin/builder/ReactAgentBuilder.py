from langchain_core.language_models.chat_models import BaseChatModel
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from langgraph.prebuilt import create_react_agent
from typing import Optional, Callable, Any
from langchain_core.tools import BaseTool


class ReactAgentBuilder(BaseWorkflowBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.tools: Optional[list[BaseTool | Callable]] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None

    async def __call__(self, **kwargs):
        try:
            name = kwargs.get("name")
            if name is None:
                raise ValueError("name가 필요합니다")
            self.name = name

            description = kwargs.get("description")
            if description is None:
                raise ValueError("description이 필요합니다")
            self.description = description

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
        except Exception as e:
            raise e

    async def build(self):
        try:
            graph = create_react_agent(
                model=self.llm,
                tools=self.tools,
                name=self.name,
                prompt=self.prompt,
            )
        except Exception as e:
            raise e
        return graph


async def register(registry):
    try:
        await registry.register(ReactAgentBuilder)
    except Exception as e:
        raise e

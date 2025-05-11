from langchain_core.language_models.chat_models import BaseChatModel
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from langchain.tools.render import render_text_description
from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from typing import Optional, Callable


class ReactAgentBuilder(BaseWorkflowBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.tools: Optional[list[BaseTool | Callable]] = []
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

            system_prompt = self.prompt
            if system_prompt is None:
                template = """
                    Answer the following questions as best you can. You have access to the following tools:

                    {tools}

                    Use the following format:

                    Question: the input question you must answer
                    Thought: you should always think about what to do
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action
                    Observation: the result of the action
                    ... (this Thought/Action/Action Input/Observation can repeat N times)
                    Thought: I now know the final answer
                    Final Answer: the final answer to the original input question

                    Begin!

                    Question: (user Input)
                    Thought:
                """
                prompt = PromptTemplate.from_template(template)
                system_prompt = prompt.partial(
                    tools=render_text_description(self.tools),
                    tool_names=", ".format(t.name for t in self.tools),
                )

            graph = create_react_agent(
                model=self.llm,
                tools=self.tools,
                name=self.name,
                prompt=system_prompt,
            )
        except Exception as e:
            raise e
        return graph


async def register(registry):
    try:
        await registry.register(ReactAgentBuilder)
    except Exception as e:
        raise e

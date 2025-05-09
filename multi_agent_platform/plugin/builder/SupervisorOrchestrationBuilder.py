from domain.builder.base_orchestrator_workflow_builder import (
    BaseOrchestratorWorkflowBuilder,
)
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph_supervisor import create_supervisor
from langgraph.graph import StateGraph
from typing import Optional, Any


class SupervisorOrchestrationBuilder(BaseOrchestratorWorkflowBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llm: Optional[BaseChatModel] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None
        self.agent_builder_list: Optional[list[BaseWorkflowBuilder]] = []

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
                raise ValueError("llms가 필요합니다.")
            self.llm = llms[0]

            prompts = kwargs.get("prompt")
            if prompts:
                self.prompt = prompts

        except Exception as e:
            raise

    async def add_agent(self, agent: BaseWorkflowBuilder) -> None:
        if not isinstance(agent, BaseWorkflowBuilder):
            raise ValueError("agent must be an instance of BaseWorkflowBuilder")
        self.agent_builder_list.append(agent)

    async def reset_agent(self) -> None:
        self.agent_builder_list = []

    async def build(self, checkpointer: Optional[Any] = None) -> StateGraph:
        try:
            print("name:", self.name)  # test
            print("prompt:", self.prompt)  # test
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
                print("agent name:", agent.name)  # test
                print("agent:", agent, "\n")  # test
                agent_list.append(await agent.build())

            self.graph = create_supervisor(
                model=self.llm,
                prompt=system_prompt,
                agents=agent_list,
                supervisor_name=self.name,
                output_mode="full_history",
            )
            compiled_graph = self.graph.compile(
                name=self.name, checkpointer=checkpointer
            )
        except Exception as e:
            raise
        return compiled_graph


async def register(registry):
    try:
        await registry.register(SupervisorOrchestrationBuilder)
    except Exception as e:
        raise

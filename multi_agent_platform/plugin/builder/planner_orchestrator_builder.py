from domain.builder.base_orchestrator_workflow_builder import (
    BaseOrchestratorWorkflowBuilder,
)
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph_supervisor import create_supervisor
from langgraph.graph.graph import CompiledGraph
from typing import Optional, Any, Callable
from langchain_core.tools import BaseTool
from typing import Annotated, List
from pydantic import BaseModel


class PlanExecute(AgentState):
    plan: Annotated[List[str], "Current plan"]


class Plan(BaseModel):
    """Sorted steps to execute the plan"""

    steps: Annotated[List[str], "Different steps to follow, should be in sorted order"]


class PlannerOrchestratorBuilder(BaseOrchestratorWorkflowBuilder):
    def __init__(self):
        super().__init__()
        self.name: Optional[str] = None
        self.llms: Optional[List[BaseChatModel]] = None
        self.prompt: Optional[str] = None
        self.description: Optional[str] = None
        self.tools: Optional[list[BaseTool | Callable]] = None
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
            self.llms = llms

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

    async def build(self, checkpointer: Optional[Any] = None) -> CompiledGraph:
        try:
            system_prompt = self.prompt
            if self.prompt is None:
                members = []
                members = [
                    f"{agent.name}: {agent.description}"
                    for agent in self.agent_builder_list
                ]
                options = ["FINISH"] + members
                default_prompt = (
                    "You are a supervisor tasked with managing a conversation between the"
                    f" following workers: {options}. Given the following mission and information,"
                    " respond with the most appropriate worker to act next."
                    " Each worker will perform a task and respond with their results and status."
                    " Use the mission and information to guide your selection."
                    " When the mission is completed successfully, you must select FINISH."
                )
                system_prompt = default_prompt.format(options=options)
            agent_list = []
            for agent in self.agent_builder_list:
                agent_list.append(await agent.build())
            self.graph = create_supervisor(
                model=self.llms[0],
                prompt=system_prompt,
                supervisor_name=self.name,
                agents=agent_list,
                output_mode="full_history",
            )

            agent_executor = self.graph.compile()

            planner_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """주어진 목표를 위해 간단한 단계별 계획을 세우세요. \n이 계획은 개별 작업을 포함해야 하며, 올바르게 실행되면 정답을 얻을 수 있습니다. 불필요한 단계를 추가하지 마세요. \n마지막 단계의 결과가 최종 답이 되어야 합니다. 각 단계에 필요한 모든 정보가 있는지 확인하세요 - 단계를 건너뛰지 마세요.""",
                    ),
                    ("placeholder", "{messages}"),
                ]
            )

            planner = planner_prompt | self.llms[1].with_structured_output(Plan)

            async def plan_step(state: PlanExecute):
                plan = await planner.ainvoke(state)
                return {"plan": plan.steps}

            async def execute_step(state: PlanExecute, config: RunnableConfig):
                plan = state["plan"]
                result: str = ""
                for step in plan:
                    task_formatted = f"""mission: {step}, information: {result}"""
                    agent_response = await agent_executor.ainvoke(
                        {"messages": [{"role": "user", "content": task_formatted}]},
                        config,
                    )
                    result = agent_response["messages"][-1].content
                return {
                    "messages": [
                        {
                            "role": "assistant",
                            "content": agent_response["messages"][-1].content,
                        }
                    ],
                }

            workflow = StateGraph(PlanExecute)
            workflow.add_node("planner", plan_step)
            workflow.add_node("execute", execute_step)
            workflow.add_edge(START, "planner")
            workflow.add_edge("planner", "execute")
            workflow.add_edge("execute", END)
            app = workflow.compile(name="planner", checkpointer=checkpointer)

        except Exception as e:
            raise
        return app


async def register(registry):
    try:
        await registry.register(PlannerOrchestratorBuilder)
    except Exception as e:
        raise

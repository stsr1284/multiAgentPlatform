from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse


from orchestration_app.domain.entities.AgentDefinition import AgentDefinition

from orchestration_app.domain.orchestrators.ManagementOrchestrator import (
    ManagementOrchestrator,
)  # test
from orchestration_app.domain.orchestrators.CollaborationOrchestrator import (
    CollaborationOrchestrator,
)  # test

from orchestration_app.domain.Builder.SupervisorAgentBuilder import (
    SupervisorAgentBuilder,
)
from langchain_openai import ChatOpenAI  # test

from langchain.agents import tool  # test

from orchestration_app.domain.registry.ToolRegistry import ToolRegistry
from orchestration_app.domain.registry.LLMRegistry import LLMRegistry
from orchestration_app.domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from orchestration_app.domain.Builder.ReactAgentBuilder import ReactAgentBuilder

from orchestration_app.utils.config import settings

router = APIRouter()

llmRegistry = LLMRegistry(
    ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=settings.OPENAI_API_KEY,
    ),
    ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=settings.OPENAI_API_KEY,
    ),
)

llm_name = ["gpt-4o-mini"]
llms = []
llms = [llmRegistry.get(name) for name in llm_name if llmRegistry.get(name) is not None]


@tool
def research_tool(topic: str) -> str:
    """A simple research tool that takes a topic and returns a research statement."""
    if not isinstance(topic, str):
        raise ValueError("Topic must be a string.")
    if not topic:
        raise ValueError("Topic cannot be empty.")
    return f"Researching the topic: {topic}"


@tool
def search_urls(urls: list[str], urllens: int):
    """A simple search tool that takes a list of URLs and returns a list of search results."""
    if not isinstance(urls, list):
        raise ValueError("URLs must be a list.")
    if not urls:
        raise ValueError("URLs cannot be empty.")
    if not all(isinstance(url, str) for url in urls):
        raise ValueError("All URLs must be strings.")
    return f"Searching the following URLs: {urls}"


toolRegistry = ToolRegistry(
    research_tool,
    search_urls,
)

tool_names = ["research_tool", "search_urls"]
tools = []
tools = [
    toolRegistry.get(name) for name in tool_names if toolRegistry.get(name) is not None
]
# tools = [toolRegistry.get("research_tool")]

print("tool Name: ", tools)

agentBuilderRegistry = AgentBuilderRegistry(
    ReactAgentBuilder(), SupervisorAgentBuilder()
)


test_agent = agentBuilderRegistry.get("reactagentbuilder")
print("test_agent:", test_agent.type)

supervisor_agent = agentBuilderRegistry.get("supervisoragentbuilder")
# agent1 = AgentDefinition(
#     llm=llmRegistry.get("gpt-4o"),
#     name="researcher_agent",
#     tools=[toolRegistry.get("research_tool")],
#     description="Transfer the user to the researcher_agent to perform research and implement the solution to the user's request.",
#     prompt="go to the planner_agent and call the research_tool",
#     config={"recursion_limit": 3},
# )
# agent2 = AgentDefinition(
#     llm=llmRegistry.get("gpt-4o-mini"),
#     name="planner_agent",
#     tools=[toolRegistry.get("search_urls")],
#     description="go to the researcher_agent and call the search_urls",
#     prompt="""
#     go to the researcher_agent and call the search_urls tool.
# """,
#     config={},
# )


async def stream_async(graph, inputs):
    async for chunk in graph.astream(inputs, stream_mode="values"):
        chunk["messages"][-1].pretty_print()
        final_message = chunk["messages"][-1]

    return final_message


@router.post("/run-agent")
async def run_orchestration(
    session: str,
    user_id: str,
    query: str,
    agent_list: list[str],
    orchestrator_type: str = "supervisor",
):
    try:
        print(
            "run_orchestration: ",
            user_id,
            " ",
            session,
            " ",
            query,
            " ",
            agent_list,
            " ",
            orchestrator_type,
        )
        question = "user your tool"
        await test_agent(llms=llms, tools=tools, names=["palnner"])
        print("1")
        print("test_agent name: ", test_agent.name)
        await supervisor_agent(
            llms=llms, names=["travelsupervisor"], agent_builder_list=[test_agent]
        )
        print("2")
        graph = await supervisor_agent.build()
        print("3")
        # result = graph.invoke(
        #     {
        #         "messages": [
        #             {
        #                 "role": "user",
        #                 "content": question,
        #             }
        #         ]
        #     }
        # )
        input = {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
        result = await stream_async(graph, input)
        print("4")
        print("run_orchestration result:", result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stream")
async def stream_orchestration(
    query: str,
):
    try:
        orchestration = ManagementOrchestrator(agent_list=agent_lists, model=llm)
        print("2")
        graph = orchestration.execute()
        input = {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }

        async def stream_async(graph, inputs):
            try:
                async for chunk in graph.astream(inputs, stream_mode="values"):
                    yield chunk["messages"][-1].content

            except Exception as e:
                yield f"data: {e}\n\n"

        print("3")
        return StreamingResponse(
            stream_async(graph, input), media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/register")
# async def register_agent(agent: RegisterAgent):
#     print("router register_agent agent:", agent, "\n")
#     return True


# @router.post("/remove")
# async def remove_agent(agent_name: str):
#     return True

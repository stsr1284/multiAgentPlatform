from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from container import (
    tool_registry,
    llm_registry,
    agent_builder_registry,
    agent_factory,
    agent_registry,
)
from domain.registry.ToolRegistry import ToolRegistry
from domain.registry.LLMRegistry import LLMRegistry
from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from domain.registry.AgentRegistry import AgentRegistry

from langgraph.graph.graph import CompiledGraph  # test


router = APIRouter()


def get_tool_registry():
    # Assuming ToolRegistry is a singleton or similar
    return tool_registry


def get_llm_registry():
    # Assuming LLMRegistry is a singleton or similar
    return llm_registry


def get_agent_builder_registry():
    # Assuming AgentBuilderRegistry is a singleton or similar
    return agent_builder_registry


def get_agent_registry():
    # Assuming AgentRegistry is a singleton or similar
    return agent_registry


@router.get("/get_tools")
async def get_tools(
    tool_registry: ToolRegistry = Depends(get_tool_registry),
    llm_registry: LLMRegistry = Depends(get_llm_registry),
    agent_builder_registry: AgentBuilderRegistry = Depends(get_agent_builder_registry),
    agent_registry: AgentRegistry = Depends(get_agent_registry),
):
    try:
        # Assuming agent_factory is defined and has a method to get tools
        print("-----------Registry Info----------")
        tools = await tool_registry.get_all()
        [print("tool: ", key, " ", value) for key, value in tools.items()]
        llms = await llm_registry.get_all()
        [print("llm: ", key, " ", value) for key, value in llms.items()]
        agent_builders = await agent_builder_registry.get_all()
        [
            print(
                "agent_builder: ",
                key,
                " ",
                value,
            )
            for key, value in agent_builders.items()
        ]
        agents = await agent_registry.get_all()
        [
            print(
                "agent_registry: ",
                key,
                " ",
                value,
            )
            for key, value in agents.items()
        ]
        print("-----------Registry Info----------")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test_agent")
async def test_agent(
    question: str,
    agent_registry: AgentRegistry = Depends(get_agent_registry),
):
    try:
        # Assuming agent_factory is defined and has a method to get tools
        builders = await agent_registry.get_all()
        agents = [await builder.build() for builder in builders.values()]
        question = question
        input = {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
        results = [await agent.ainvoke(input) for agent in agents]
        [print(result["messages"][-1].pretty_print(), "\n\n") for result in results]

        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        agent_list = await agent_factory.create_agents_from_json(json_data)
        good_agent_list = [await agent.build() for agent in agent_list]
        question = "user your tool"
        input = {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
        results = [agent.invoke(input) for agent in good_agent_list]
        # [print(result["messages"][-1].content, "\n\n") for result in results]
        [print(result["messages"][-1].pretty_print(), "\n\n") for result in results]

        return True
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

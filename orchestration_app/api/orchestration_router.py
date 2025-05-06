from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import (
    ResumeAStreamStrategy,
)
from domain.entyties.UserInput import OrchestrationInput, UserInput
from application.orchestration_service import OrchestrationService
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from fastapi import APIRouter, Depends
from application.resume_service import ResumeService
from fastapi.responses import StreamingResponse
from .dependencies import (
    get_orchestration_astream_strategy,
    get_orchestration_service,
    get_resume_service,
    get_checkpointer,
    get_resume_astream_strategy,
)


router = APIRouter()


# @router.get("/get_tools")
# async def get_tools(
#     tool_registry: ToolRegistry = Depends(get_tool_registry),
#     llm_registry: LLMRegistry = Depends(get_llm_registry),
#     agent_builder_registry: AgentBuilderRegistry = Depends(get_agent_builder_registry),
#     agent_registry: AgentRegistry = Depends(get_agent_registry),
# ):
#     try:
#         print("-----------Registry Info----------")
#         tools = await tool_registry.get_all()
#         [print("tool: ", key, " ", value) for key, value in tools.items()]
#         llms = await llm_registry.get_all()
#         [print("llm: ", key, " ", value) for key, value in llms.items()]
#         agent_builders = await agent_builder_registry.get_all()
#         [
#             print(
#                 "agent_builder: ",
#                 key,
#                 " ",
#                 value,
#             )
#             for key, value in agent_builders.items()
#         ]
#         agents = await agent_registry.get_all()
#         [
#             print(
#                 "agent_registry: ",
#                 key,
#                 " ",
#                 value,
#             )
#             for key, value in agents.items()
#         ]
#         print("-----------Registry Info----------")
#         return True
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/test_agent")
# async def test_agent(
#     question: str,
#     agent_registry: AgentRegistry = Depends(get_agent_registry),
# ):
#     try:
#         # Assuming agent_factory is defined and has a method to get tools
#         builders = await agent_registry.get_all()
#         agents = [await builder.build() for builder in builders.values()]
#         question = question
#         input = {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": question,
#                 }
#             ]
#         }
#         results = [await agent.ainvoke(input) for agent in agents]
#         [print(result["messages"][-1].pretty_print(), "\n\n") for result in results]

#         return True
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/astream")
async def run_orchestration(
    orchestration_input: OrchestrationInput,
    checkpointer: AsyncPostgresSaver = Depends(get_checkpointer),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    strategy: OrchestrationAStreamStrategy = Depends(
        get_orchestration_astream_strategy
    ),
):
    astream = await orchestration_service.run(
        strategy, orchestration_input, checkpointer
    )
    return StreamingResponse(astream, media_type="text/event-stream")


@router.post("/chat/astream_resume")
async def resume_orchestration(
    user_input: UserInput,
    resume_service: ResumeService = Depends(get_resume_service),
    strategy: ResumeAStreamStrategy = Depends(get_resume_astream_strategy),
):
    astream = await resume_service.run(strategy, user_input)
    return StreamingResponse(astream, media_type="text/event-stream")


# @router.get("/stream")
# async def stream_orchestration(
#     query: str,
# ):
#     try:
#         orchestration = ManagementOrchestrator(agent_list=agent_lists, model=llm)
#         print("2")
#         graph = orchestration.execute()
#         input = {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": query,
#                 }
#             ]
#         }

#         async def stream_async(graph, inputs):
#             try:
#                 async for chunk in graph.astream(inputs, stream_mode="values"):
#                     yield chunk["messages"][-1].content

#             except Exception as e:
#                 yield f"data: {e}\n\n"

#         print("3")
#         return StreamingResponse(
#             stream_async(graph, input), media_type="text/event-stream"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# agent_list = await agent_factory.create_agents_from_json(json_data)
# good_agent_list = [await agent.build() for agent in agent_list]
# question = "user your tool"
# input = {
#     "messages": [
#         {
#             "role": "user",
#             "content": question,
#         }
#     ]
# }
# results = [agent.invoke(input) for agent in good_agent_list]
# # [print(result["messages"][-1].content, "\n\n") for result in results]
# [print(result["messages"][-1].pretty_print(), "\n\n") for result in results]


# @router.post("/register")
# async def register_agent(agent: RegisterAgent):
#     print("router register_agent agent:", agent, "\n")
#     return True


# @router.post("/remove")
# async def remove_agent(agent_name: str):
#     return True

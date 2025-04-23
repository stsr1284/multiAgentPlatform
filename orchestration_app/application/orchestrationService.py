from pydantic import Field
from domain.interfaces.ToolListProvider import ToolListProvider
from domain.interfaces.brokerInterface import BrokerInterface
from shared.loggin_config import logger #test


from langgraph.prebuilt import create_react_agent # test
from langchain_openai import ChatOpenAI # test
from langchain_core.tools import BaseTool # test
from langchain_core.runnables import RunnableConfig # 
import time # test
import tracemalloc # test


class OrchestrationService:
    toolList: ToolListProvider = Field(default_factory=ToolListProvider, description="Tool list instance")
    # broker: BrokerInterface = Field(default_factory=BrokerInterface, description="Broker instance")
    graph: str = Field(default="orchestration", description="Graph name")

    def __init__(self, toolList: ToolListProvider, broker: BrokerInterface):
        self.toolList = toolList
        self.broker = broker


    # graph로 변환
    async def plan_and_execute(self, user_input: str):
        logger.info("orchestration plan_and_execute")
        plans = await self._create_plans(user_input)

        for plan in plans:
            logger.info(f"Plan name: {plan}")
            # result = plan.invoke({"location": user_input})
            # logger.info(f"Plan result: {result}")

        all_tools: list[BaseTool] = []
        for server_tools in plans.values():
            all_tools.extend(server_tools)
        logger.info(f"toolBase_list: {all_tools}")


        config=RunnableConfig(
            recursion_limit=3,
        ),

        # test
        logger.info("creat model")
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key="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")
        logger.info("create react agent")


        # graph = create_react_agent(model, tools=all_tools, config_schema=config)
        tracemalloc.start()

        # 시간 측정 시작
        start_time = time.perf_counter()

        # create_react_agent 호출
        graphs = []
        for i in range(1000):
            logger.info(f"Creating react agent {i+1}")
            graph = create_react_agent(model, tools=all_tools, config_schema=config)
            graphs.append(graph)
        print("\ngraphs size:",graphs.__sizeof__(), "\n")

        # 시간 측정 종료
        end_time = time.perf_counter()

        # 메모리 사용량 측정
        current, peak = tracemalloc.get_traced_memory()

        # 메모리 추적 종료
        tracemalloc.stop()

        # 결과 출력
        print(f"빌드 시간: {end_time - start_time:.4f}초")
        print(f"현재 메모리 사용량: {current / 1024:.2f} KB")
        print(f"최대 메모리 사용량: {peak / 1024:.2f} KB")














        inputs = {"messages": [("user", f"{user_input}")]}
        logger.info("invoke graph")
        response = await graph.ainvoke(inputs)
        result = response["messages"][-1].content
        logger.info(f"orchestration plan_and_execute result: {result}")
        #test 
        return  True

    async def _create_plans(self, user_input: str) -> dict[str, list[BaseTool]]:
        logger.info("orchestration _create_plans")
        toolList =  await self.get_toolList()
        ## 여기서 plan 작성해야됨
        return toolList ## 임시

    async def get_toolList(self):
        return  await self.toolList.get_tool_list()

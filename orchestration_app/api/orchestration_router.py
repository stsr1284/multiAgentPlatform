from fastapi import APIRouter, HTTPException
from application.orchestrationService import OrchestrationService
from application.brokerService import Broker
from infrastructure.observers.ToolList import ToolList
from domain.entities.RegisterAgent import RegisterAgent
from dotenv import load_dotenv

load_dotenv()



router = APIRouter()


toolListProvider = ToolList()  # ToolListProvider 인스턴스 생성

broker = Broker(tool_list=toolListProvider)  # BrokerInterface 인스턴스 생성

service = OrchestrationService(toolList=toolListProvider, broker=broker)  # 의존성 주입(DI) 방식으로 교체 가능


@router.post("/run-agent")
async def run_agent(query: str):
    try:
        print("router run-agent query:", query)
        result = await service.plan_and_execute(query)
        print("router run-agent result:", result)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register_agent(agent: RegisterAgent):
    print("router register_agent agent:", agent, "\n")
    return await broker.register_agent(agent)

@router.post("/remove")
async def remove_agent(agent_name: str):
    return broker.unregister_agent(agent_name)

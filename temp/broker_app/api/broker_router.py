from fastapi import APIRouter, HTTPException
from application.broker_service import BrokerService

router = APIRouter()
service = BrokerService()  # DI 방식으로 교체 가능

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/execute")
async def execute_agent(plan: dict):
    try:
        result = await service.execute_agent(plan)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register_agent(agent_info: dict):
    try:
        service.register_agent(agent_info)
        return {"status": "registered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{agent_id}")
async def delete_agent(agent_id: str):
    try:
        service.delete_agent(agent_id)
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/toolList")
async def get_tool_list():
    try:
        tool_list = service.get_tool_list()
        return {"toolList": tool_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

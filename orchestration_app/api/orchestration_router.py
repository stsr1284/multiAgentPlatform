from fastapi import APIRouter, HTTPException
from application.orchestration_service import OrchestrationService

router = APIRouter()
service = OrchestrationService()  # 의존성 주입(DI) 방식으로 교체 가능


@router.post("/run-agent")
async def run_agent(query: str):
    try:
        result = await service.run_agent(query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import httpx
from domain.entities.plan import Plan
from infrastructure.broker_client import BrokerClient
from shared.exceptions import BrokerUnavailableException


# 내부 LLM fallback (단순 예시)
async def call_internal_llm(query: str) -> str:
    # 내부 OpenAPI LLM 호출 예시
    return f"LLM fallback answer for: {query}"


class OrchestrationService:
    def __init__(self):
        self.broker_client = BrokerClient()

    async def run_agent(self, query: str) -> str:
        # 1. 내부 LLM을 통해 외부 에이전트 필요성 판단 (단순 예시)
        requires_external = "외부" in query or "agent" in query
        if requires_external:
            # 2. Broker와의 Health Check (또는 toolList 요청)
            if not await self.broker_client.is_available():
                # Broker가 정상 작동하지 않을 경우 fallback
                return await call_internal_llm(query)
            # 3. Plan 생성 (Domain Entity 사용)
            plan = Plan.create_plan(query)
            # 4. Broker에게 실행 요청
            result = await self.broker_client.execute_agent(plan)
            return result
        else:
            # 외부 에이전트가 필요 없으면 단순 처리
            return "내부 처리 결과: 외부 에이전트 불필요"

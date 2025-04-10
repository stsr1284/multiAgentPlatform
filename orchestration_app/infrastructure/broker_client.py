import httpx
from shared.exceptions import BrokerUnavailableException

BROKER_BASE_URL = "http://localhost:9000"  # 브로커 애플리케이션 주소


class BrokerClient:
    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{BROKER_BASE_URL}/broker/health")
                return response.status_code == 200
        except Exception:
            return False

    async def execute_agent(self, plan) -> str:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # plan을 JSON 직렬화하여 전달 (예시)
                response = await client.post(
                    f"{BROKER_BASE_URL}/broker/execute", json={"plan": plan.steps}
                )
                if response.status_code != 200:
                    raise BrokerUnavailableException("Broker 실행 실패")
                return response.json().get("result", "")
        except Exception as e:
            raise BrokerUnavailableException(str(e))

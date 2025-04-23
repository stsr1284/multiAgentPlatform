# MCP와의 통신을 담당하는 클라이언트 (예시)
import httpx

class MCPClient:
    async def call_agent(self, agent_id: str, task: str) -> str:
        # 실제 MCP 호출 로직 구현
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://mcp/execute", json={"agent_id": agent_id, "task": task})
            return response.json().get("result", "")

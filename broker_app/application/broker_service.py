from infrastructure.mcp_client import MCPClient
from domain.entities.agent import Agent

# 예시로 메모리 내 에이전트 저장소
AGENT_REGISTRY = {}

class BrokerService:
    def __init__(self):
        self.mcp_client = MCPClient()

    async def execute_agent(self, plan: dict) -> str:
        # plan 내 각 step에 대해 에이전트 실행 (간단 예시)
        results = []
        for step in plan.get("plan", []):
            agent_id = step.get("agent")
            agent = AGENT_REGISTRY.get(agent_id)
            if agent:
                result = agent.run(step.get("task"))
                results.append(result)
            else:
                results.append(f"Agent {agent_id} not found")
        return " | ".join(results)

    def register_agent(self, agent_info: dict):
        agent = Agent.from_dict(agent_info)
        AGENT_REGISTRY[agent.agent_id] = agent

    def delete_agent(self, agent_id: str):
        if agent_id in AGENT_REGISTRY:
            del AGENT_REGISTRY[agent_id]

    def get_tool_list(self) -> list:
        # 단순 예시: 등록된 모든 agent의 도구 모음
        tools = []
        for agent in AGENT_REGISTRY.values():
            tools.extend(agent.tools)
        return list(set(tools))

from .ToolRegistry import ToolRegistry

# 에이전트 실행기
class AgentExecutor:
    def __init__(self, agent_registry: ToolRegistry):
        self._agent_registry = agent_registry
    
    async def execute(self, plan: dict):
        agent_id = plan["name"]
        agent = self._agent_registry.get_tool(agent_id)
        print("AgentExecutor execute agent:", agent, "\n\n")
        
        if not agent:
            raise ValueError(f"Agent {agent_id} not registered")
        
        print("AgentExecutor execute finish agent:", agent, "\n\n")
        return await self._call_agent(agent.endpoint, plan["name"])
        # return await self._call_agent(agent.endpoint, plan["params"])
    
    async def _call_agent(self, endpoint: str, params: dict):
        # 실제 구현
        return {"status": "success", "data": params}
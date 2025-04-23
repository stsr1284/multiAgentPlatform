class Agent:
    def __init__(self, agent_id: str, name: str, tools: list):
        self.agent_id = agent_id
        self.name = name
        self.tools = tools

    def run(self, task: str) -> str:
        # 외부 Agent는 MCP를 통해 호출하는 로직이 추가될 수 있음
        return f"{self.name} executed task: {task}"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            agent_id=data.get("agent_id"),
            name=data.get("name"),
            tools=data.get("tools", [])
        )

from infrastructure.observers.observerManager import ObserverManager
from domain.interfaces.ToolManager import ToolManager
from domain.entities.RegisterAgent import RegisterAgent
from langchain_core.tools import BaseTool # test
from typing import Optional



from infrastructure.MCPClientAdapter import MultiServerMCPClientAdapter
from .MCPManager import MCPManager

# 에이전트 레지스트리
class ToolRegistry(ToolManager):
    def __init__(self, observer_manager: ObserverManager):
        self._observer_manager = observer_manager
        self.mcp_manager = MCPManager(MultiServerMCPClientAdapter())
        self._toolList: dict[str, list[BaseTool]] = {}# test
        self.mcp_config: dict = {}
    
    async def register_tool(self, agent: RegisterAgent) -> None:
        print("AgentRegistry register_agent:", agent)
        print("agent type:", agent.type)

        if agent.type == "mcp":
            print("agent type is mcp:", agent.config)
            valid_result = await self.mcp_manager.validate_mcp_config(agent.config)
            if not valid_result or len(valid_result) == 0:
                print("MCP 서버 설정이 유효하지 않습니다.")
                return
            print("MCP 서버 설정이 유효합니다.")
            await self.mcp_manager.connect_server(valid_result)
            print("MCP 서버 연결됨:", valid_result)
            self._toolList.update(await self.mcp_manager.get_all_tools_as_dict())
            pretty_print_toolbased(self._toolList)
        else:
            print("agent type is not mcp:", agent.config)
            # 다른 유형의 에이전트 처리 로직 추가
            return 

        print("\nAgentRegistry register_agent complete\n")
        await self._notify_changes()
    
    async def unregister_tool(self, server_name: str) -> None:
        if server_name in self._toolList:
            await self.mcp_manager.disconnect_server(server_name)
            await self._notify_changes()
    
    def get_tool(self, agent_id: str) -> Optional[RegisterAgent]:
        return self._toolList.get(agent_id)
    
    async def _notify_changes(self) -> None:
        await self._observer_manager.notify_observers(self._toolList)
    

def pretty_print_toolbased(tool_list: dict[str, list[BaseTool]]) -> None:
    for tool in tool_list:
        print(f"Tool Name: {tool}")
        # print(f"Tool Description: {tool.description}")
        # print(f"Tool Metadata: {tool.metadata}")
        print("-" * 40)
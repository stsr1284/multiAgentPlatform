from domain.interfaces.ClientInterface import ClientInterface
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from mcp import ClientSession

class MultiServerMCPClientAdapter(ClientInterface):
    def __init__(self) -> None:
        self.mcp_client: MultiServerMCPClient = None


    async def _mcp_client_init(self, config) -> None:
        self.mcp_client = MultiServerMCPClient(config)
        await self.mcp_client.__aenter__()
    
    async def connect(self, connections:dict) -> None:
        try:
            if self.mcp_client is None:
                await self._mcp_client_init(connections)
            else:
                for server_name, connection in connections.items():
                    await self.mcp_client.connect_to_server(server_name, **connection)
        except Exception:
            await self.mcp_client.exit_stack.aclose()
            raise

    async def disconnect(self, server_name: str) -> None:
        if server_name in self.mcp_client.sessions:
            session = self.mcp_client.sessions.pop(server_name)
            await session.__aexit__(None, None, None)  # 세션 종료
        if server_name in self.mcp_client.server_name_to_tools:
            self.mcp_client.server_name_to_tools.pop(server_name)  # 세션 목록 제거


    def get_all_tools_as_list(self) -> list[BaseTool]:
        if self.mcp_client is None:
            return []
        return self.mcp_client.get_tools()
    
    async def get_all_tools_as_dict(self) -> dict[str, list[BaseTool]]:
        if self.mcp_client is None:
            return {}
        return self.mcp_client.server_name_to_tools

    async def close_all_connections(self) -> None:
        if self.mcp_client is not None:
            try:
                await self.mcp_client.__aexit__(None, None, None)
                self.mcp_client = None
            except Exception as e:
                print(f"MCP 클라이언트 종료 중 오류: {str(e)}")
                raise

    def get_sessions(self) -> dict[str, ClientSession]:
        if self.mcp_client is None:
            return {}
        return self.mcp_client.sessions
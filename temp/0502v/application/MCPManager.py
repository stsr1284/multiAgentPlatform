from infrastructure.MCPClientAdapter import ClientInterface
from langchain_core.tools import BaseTool

class MCPManager:
    def __init__(self, client_adapter: ClientInterface):
        self.client_adapter = client_adapter

    async def connect_server(self, config: dict) -> None:
        """MCP 서버 연결"""
        await self.client_adapter.connect(config)

    async def disconnect_server(self, server_name: str) -> None:
        """MCP 서버 연결 해제"""
        await self.client_adapter.disconnect(server_name)

    async def cleanup_mcp_client(self) -> None:
        """MCP 클라이언트 종료"""
        await self.client_adapter.close_all_connections()

    def get_all_tools_as_list(self) -> list[BaseTool]:
        return self.client_adapter.get_all_tools_as_list()
    
    async def get_all_tools_as_dict(self) -> dict[str, list[BaseTool]]:
        return await self.client_adapter.get_all_tools_as_dict()
    
    # 추후에 pydantic 으로 빼서 검증함
    async def validate_mcp_config(self, config: dict) -> dict:
        # mcpServers 형식인지 확인하고 처리
        if "mcpServers" in config:
            # mcpServers 안의 내용을 최상위로 이동
            config = config["mcpServers"]
            print("'mcpServers' 형식이 감지되었습니다. 자동으로 변환합니다.")

        # 입력된 도구 수 확인
        if len(config) == 0:
            print("최소 하나 이상의 도구를 입력해주세요.")
        else:
            cur_sessions = self.client_adapter.get_sessions()
            # 모든 도구에 대해 처리
            success_tools = {}
            for tool_name, tool_config in config.items():
                # URL 필드 확인 및 transport 설정
                if "url" in tool_config:
                    # URL이 있는 경우 transport를 "sse"로 설정
                    tool_config["transport"] = "sse"
                    print(
                        f"'{tool_name}' 도구에 URL이 감지되어 transport를 'sse'로 설정했습니다."
                    )
                elif "transport" not in tool_config:
                    # URL이 없고 transport도 없는 경우 기본값 "stdio" 설정
                    tool_config["transport"] = "stdio"

                # 필수 필드 확인
                if ("command" not in tool_config and "url" not in tool_config):
                    print(
                        f"'{tool_name}' 도구 설정에는 'command' 또는 'url' 필드가 필요합니다."
                    )
                elif "command" in tool_config and "args" not in tool_config:
                    print(
                        f"'{tool_name}' 도구 설정에는 'args' 필드가 필요합니다."
                    )
                elif "command" in tool_config and not isinstance(tool_config["args"], list):
                    print(
                        f"'{tool_name}' 도구의 'args' 필드는 반드시 배열([]) 형식이어야 합니다."
                    )
                else:
                    print("validation_config 현재 보고있는 server: ", tool_name)
                    print("validation_config 현재 session keys: ", cur_sessions.keys())
                    if tool_name in cur_sessions:
                        print(
                            f"'{tool_name}' 도구는 이미 등록되어 있습니다."
                        )
                        continue
                    # self.mcp_config[tool_name] = tool_config
                    success_tools[tool_name] = tool_config

            # 성공 메시지
            if success_tools:
                # 잘못된 에러에 대한 반환 처리
                if len(success_tools) == 1:
                    print(
                        f"{success_tools.keys()} 도구가 추가되었습니다. 적용하려면 '설정 적용하기' 버튼을 눌러주세요."
                    )
                else:
                    tool_names = ", ".join(success_tools)
                    print(
                        f"총 {len(success_tools)}개 도구({tool_names})가 추가되었습니다. 적용하려면 '설정 적용하기' 버튼을 눌러주세요."
                    )
            return success_tools

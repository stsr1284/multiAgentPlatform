# weather_server.py
from mcp.server.fastmcp import FastMCP
import uvicorn # 필요: pip install uvicorn

# mcp = FastMCP("Weather")
mcp = FastMCP(
    "Weather",  # Name of the MCP server
    instructions="You are a weather assistant that can answer questions about the weather in a given location.",  # Instructions for the LLM on how to use this tool
    host="0.0.0.0",  # Host address (0.0.0.0 allows connections from any IP)
    port=8005,  # Port number for the server
)

@mcp.tool()
async def get_weather(location: str) -> str:
    """위치에 대한 날씨 정보를 가져옵니다."""
    print(f"Executing get_weather({location})")
    # 실제 시나리오에서는 날씨 API를 호출합니다
    return f"{location}에서는 항상 맑습니다."

if __name__ == "__main__":
    # SSE 전송을 사용하여 서버 실행(uvicorn과 같은 ASGI 서버가 필요)
    # mcp 라이브러리는 SSE를 위해 암묵적으로 FastAPI 앱을 생성합니다.
    # 기본적으로 포트 8000의 /sse 엔드포인트에서 실행됩니다.
    print("포트 8005에서 SSE를 통해 Weather MCP 서버 시작 중...")
    # uvicorn.run(mcp.app, host="0.0.0.0", port=8000) # 수동으로 실행할 수 있습니다
    mcp.run(transport="sse") # 또는 mcp.run 편의 기능 사용

# {
#   "type": "mcp",
#   "config": {
#     "weather_service": {
#             "transport": "sse",
#             "url": "http://0.0.0.0:8005/sse"
#     }
#   }
# }

# {
#   "type": "mcp",
#   "config": {
#   "mcpServers": {
#     "mcp-server-hotnews": {
#       "command": "npx",
#       "args": [
#         "-y",
#         "@smithery/cli@latest",
#         "run",
#         "@wopal/mcp-server-hotnews",
#         "--key",
#         "7cf2f38d-fe3f-4b91-afb5-c48e773caf87"
#       ]
# }
#     }
#   }
# }
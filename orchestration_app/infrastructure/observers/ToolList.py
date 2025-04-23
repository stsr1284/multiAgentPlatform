import asyncio
from domain.interfaces.Observer import Observer
from domain.interfaces.ToolListProvider import ToolListProvider
from pydantic import Field

from langchain_core.tools import BaseTool # test
from shared.loggin_config import logger

class ToolList(Observer, ToolListProvider):
    """도구 목록 옵저버 구현"""

    # toolList: List[Dict] = Field(default_factory=list, description="도구 목록")
    toolList:  dict[str, list[BaseTool]] = Field(default_factory=dict[str, list[BaseTool]], description="도구 목록")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lock = asyncio.Lock()
    
    async def update(self, data:  dict[str, list[BaseTool]]) -> None:
        """상태 업데이트 처리"""
        async with self._lock:
            for tool in data:
                logger.info(f"Tool Name: {tool}")
            self.toolList = data
    
    async def get_tool_list(self) ->  dict[str, list[BaseTool]]:
        """도구 목록 조회 (인터페이스 메서드 구현)"""
        async with self._lock:
            return self.toolList
from abc import ABC, abstractmethod

# 도구 목록 제공자 인터페이스
class ToolListProvider(ABC):
    @abstractmethod
    async def get_tool_list(self):
        pass

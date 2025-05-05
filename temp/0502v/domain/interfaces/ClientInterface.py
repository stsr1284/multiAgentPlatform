from abc import ABC, abstractmethod
from langchain_core.tools import BaseTool
from mcp import ClientSession


class ClientInterface(ABC):
    @abstractmethod
    async def connect(self, config: dict) -> None:
        """서버에 연결"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """서버 연결 해제"""
        pass

    @abstractmethod
    def get_all_tools_as_list(self) -> list[BaseTool]:
        """모든 도구 목록을 리스트 형태로 가져오기"""
        pass

    @abstractmethod
    async def get_all_tools_as_dict(self) -> dict[str, list[BaseTool]]:
        """모든 도구 목록을 딕셔너리 형태로 가져오기"""
        pass

    @abstractmethod
    async def close_all_connections(self) -> None:
        """ 모든 클라이언트 종료 """
        pass

    @abstractmethod
    def get_sessions(self) -> dict[str, ClientSession]:
        """현재 활성화된 세션 목록 반환"""
        pass


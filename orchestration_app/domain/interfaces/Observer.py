from abc import ABC, abstractmethod


class Observer(ABC):
    """옵저버 인터페이스 - 상태 변경 알림을 받는 객체"""

    @abstractmethod
    async def update(self, data: str) -> None:
        """상태 변경시 호출되는 메서드"""
        pass

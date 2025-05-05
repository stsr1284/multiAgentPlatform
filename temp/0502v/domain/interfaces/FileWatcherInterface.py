from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Awaitable
from watchfiles import Change  # Change가 올바르게 import되어야 합니다.


class FileWatcherInterface(ABC):

    @abstractmethod
    def register_handler(
        self, handler: Callable[[Change, Path], Awaitable[None]]
    ) -> None:
        """
        변경 사항이 감지되었을 때 호출될 handler를 등록합니다.
        handler는 Change 객체와 변경된 Path를 인자로 받는 비동기 함수입니다.
        """
        pass

    @abstractmethod
    async def watch(self) -> None:
        """
        파일 변경 사항을 감시하고 등록된 handler들을 실행합니다.
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """
        파일 감시를 중지합니다.
        """
        pass

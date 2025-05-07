from domain.interfaces.file_watcher_Interface import FileWatcherInterface
from shared.loggin_config import logger
from typing import Callable, Awaitable
from watchfiles import awatch, Change
from pathlib import Path
import asyncio


class FileWatcher(FileWatcherInterface):
    def __init__(self, watch_path: str):
        self.watch_path = Path(watch_path).resolve()
        self.handlers: list[Callable[[Change, Path], Awaitable[None]]] = []
        self._stop_event = asyncio.Event()

    def register_handler(self, handler: Callable[[Change, Path], Awaitable[None]]):
        self.handlers.append(handler)

    async def watch(self):
        async for changes in awatch(self.watch_path):
            if self._stop_event.is_set():
                break
            for change, path_str in changes:
                path = Path(path_str).resolve()
                for handler in self.handlers:
                    if not callable(handler):
                        logger.warning(f"Handler {handler} is not callable")
                        continue
                    try:
                        await handler(change, path)
                    except Exception as e:
                        logger.error(f"Error in handler {handler}: {e}")

    async def stop(self):
        self._stop_event.set()

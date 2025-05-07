from domain.interfaces import file_watcher_Interface
from domain.interfaces import setup_agent_system_Interface
import asyncio


class InitializeService:
    def __init__(
        self,
        file_watcher: file_watcher_Interface,
        setup_agent_system: setup_agent_system_Interface,
    ):
        self.file_watcher = file_watcher
        self.setup_agent_system = setup_agent_system
        self._watcher_task = None

    async def setup_and_watcher_start(self):
        await self.setup_agent_system.setup_agent_system()
        self._watcher_task = asyncio.create_task(self.file_watcher.watch())

    async def stop(self):
        await self.file_watcher.stop()
        if self._watcher_task:
            self._watcher_task.cancel()
            try:
                await self._watcher_task
            except asyncio.CancelledError:
                pass

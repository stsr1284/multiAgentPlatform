from abc import ABC, abstractmethod
from shared.loggin_config import logger
import asyncio


class BaseRegistry(ABC):
    def __init__(self, *items):
        self.items_map = {}
        self._lock = asyncio.Lock()
        self.items_map = {self.get_item_name(item): item for item in items}

    @abstractmethod
    def get_item_name(self, item):
        pass

    async def register(self, item) -> None:
        async with self._lock:
            name = self.get_item_name(item)
            if name in self.items_map:
                logger.warning(
                    f"Item {name} already exists in {self.__class__.__name__}"
                )
                return
            self.items_map[name] = item
            logger.info(f"Registering item {name} in {self.__class__.__name__}")

    async def get(self, name: str):
        async with self._lock:
            item = self.items_map.get(name)
            if item is None:
                raise ValueError(f"{name} not found in {self.__class__.__name__}")
            logger.info(f"Item {name} found in {self.__class__.__name__}")
            return item

    async def get_all(self):
        async with self._lock:
            return {name: item for name, item in self.items_map.items()}

    async def unregister(self, name: str):
        async with self._lock:
            item = self.items_map.pop(name, None)
            if item is None:
                raise ValueError(f"{name} not found in {self.__class__.__name__}")
            logger.info(f"Item {name} removed from {self.__class__.__name__}")

from domain.registry.base_registry import BaseRegistry
from domain.builder.base_builder import BaseBuilder
from shared.loggin_config import logger
from typing import List


class AgentRegistry(BaseRegistry):

    def get_item_name(self, builder: BaseBuilder) -> str:
        return builder.name

    async def reset(self, items: List[BaseBuilder]) -> None:
        async with self._lock:
            self.items_map.clear()
            logger.info(f"All items cleared from {self.__class__.__name__}")
            self.items_map.update(
                {
                    self.get_item_name(item): item
                    for item in items
                    if self.get_item_name(item) not in self.items_map
                }
            )

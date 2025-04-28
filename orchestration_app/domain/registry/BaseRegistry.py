from abc import ABC, abstractmethod
from orchestration_app.shared.loggin_config import logger


class BaseRegistry(ABC):
    def __init__(self, *items):
        self.items = items
        self.items_map = {self.get_item_name(item): item for item in items}

    @abstractmethod
    def get_item_name(self, item):
        pass

    def register(self, item) -> None:
        self.items_map[self.get_item_name(item)] = item

    def get(self, name: str):
        item = self.items_map.get(name)
        if item is None:
            raise ValueError(f"{name} not found in {self.__class__.__name__}")
        logger.info(f"Item {name} found in {self.__class__.__name__}")
        return item

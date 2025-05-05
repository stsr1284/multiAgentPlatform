from .BaseRegistry import BaseRegistry
from domain.entyties.InterruptThreadGraph import InterruptThreadGraph


class GraphRegistry(BaseRegistry):
    def get_item_name(self, item):
        if isinstance(item, InterruptThreadGraph):
            return item.thread_id
        else:
            raise ValueError("Item is not an InterruptThreadGraph")

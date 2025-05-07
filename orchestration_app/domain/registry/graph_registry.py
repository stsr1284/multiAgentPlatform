from domain.entyties.interrupt_thread_graph import InterruptThreadGraph
from .base_registry import BaseRegistry


class GraphRegistry(BaseRegistry):
    def get_item_name(self, item):
        if isinstance(item, InterruptThreadGraph):
            return item.thread_id
        else:
            raise ValueError("Item is not an InterruptThreadGraph")

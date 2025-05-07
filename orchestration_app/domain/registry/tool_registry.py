from domain.registry.base_registry import BaseRegistry


class ToolRegistry(BaseRegistry):
    def get_item_name(self, tool):
        return tool.get_name()

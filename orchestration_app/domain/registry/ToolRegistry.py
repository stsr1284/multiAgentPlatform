from orchestration_app.domain.registry.BaseRegistry import BaseRegistry


class ToolRegistry(BaseRegistry):
    def get_item_name(self, tool):
        return tool.get_name()

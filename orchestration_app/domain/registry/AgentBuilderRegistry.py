from orchestration_app.domain.registry.BaseRegistry import BaseRegistry
from orchestration_app.domain.Builder.BaseBuilder import BaseBuilder


class AgentBuilderRegistry(BaseRegistry):
    def get_item_name(self, builder: BaseBuilder) -> str:
        return builder.type

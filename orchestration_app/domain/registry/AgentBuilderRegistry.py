from domain.registry.BaseRegistry import BaseRegistry
from domain.builder.base_workflow_builder import BaseWorkflowBuilder
from shared.loggin_config import logger


class AgentBuilderRegistry(BaseRegistry):

    def get_item_name(self, builder_cls: BaseWorkflowBuilder) -> str:
        temp_instance = builder_cls()
        return temp_instance.type

    async def get(self, name: str) -> BaseWorkflowBuilder:
        async with self._lock:
            builder_cls = self.items_map.get(name)
            if builder_cls is None:
                raise ValueError(f"{name} not found in {self.__class__.__name__}")
            logger.info(f"Item {name} found in {self.__class__.__name__}")
            return builder_cls()

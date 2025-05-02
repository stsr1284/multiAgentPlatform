from domain.registry.BaseRegistry import BaseRegistry
from domain.Builder.BaseBuilder import BaseBuilder
from shared.loggin_config import logger


class AgentBuilderRegistry(BaseRegistry):

    def get_item_name(self, builder_cls: BaseBuilder) -> str:
        temp_instance = builder_cls()  # 임시 인스턴스 생성
        return temp_instance.type

    async def get(self, name: str) -> BaseBuilder:
        async with self._lock:
            builder_cls = self.items_map.get(name)
            if builder_cls is None:
                raise ValueError(f"{name} not found in {self.__class__.__name__}")
            logger.info(f"Item {name} found in {self.__class__.__name__}")
            return builder_cls()  # 새 인스턴스 만들어서 리턴


# class AgentBuilderRegistry(BaseRegistry):
#     def __init__(self, *items):
#         # items는 Builder 클래스 (ex. ReactAgentBuilder)여야 함
#         self.items = items
#         self.items_map = {self.get_item_name(item): item for item in items}

#     def get_item_name(self, builder_cls: type[BaseBuilder]) -> str:
#         """builder 클래스에서 타입 이름을 추출"""
#         temp_instance = builder_cls()  # 임시 인스턴스 생성
#         return temp_instance.type

#     def get(self, name: str) -> BaseBuilder:
#         """name에 맞는 Builder 인스턴스를 새로 생성해서 반환"""
#         builder_cls = self.items_map.get(name)
#         if builder_cls is None:
#             raise ValueError(f"{name} not found in {self.__class__.__name__}")
#         logger.info(f"Item {name} found in {self.__class__.__name__}")
#         return builder_cls()  # 새 인스턴스 만들어서 리턴

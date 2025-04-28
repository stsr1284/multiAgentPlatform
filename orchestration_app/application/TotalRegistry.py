from shared.loggin_config import logger  # test
from langchain_core.language_models.chat_models import BaseChatModel  # llm Registry



class LLMRegistry(Registry):

    def __init__(self, *llms):
        self.llms = llms
        self.llms_map = {llm.model_name: llm for llm in llms}

    def register(self, llm: BaseChatModel) -> None:
        self.llms_map[llm.model_name] = llm
        logger.info(f"Registered {llm.model_name} in {self.__name__}")

    def get(self, name: str) -> any:
        item = self.llms_map.get(name)
        if item is None:
            logger.error(f"{name} not found in {self.__name__}")
            raise ValueError(f"{name} not found in {self.__name__}")
        return item


class ToolRegistry(Registry):
    pass


class AgentBuilderRegistry(Registry):
    pass

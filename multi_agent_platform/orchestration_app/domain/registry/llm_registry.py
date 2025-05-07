from domain.registry.base_registry import BaseRegistry


class LLMRegistry(BaseRegistry):
    def get_item_name(self, llm):
        return llm.model_name

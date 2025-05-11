from domain.registry.base_registry import BaseRegistry


class LLMRegistry(BaseRegistry):
    def get_item_name(self, llm):
        if hasattr(llm, "name"):
            return llm.name
        else:
            raise ValueError("LLM does not have a model name or model attribute.")

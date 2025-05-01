from domain.registry.BaseRegistry import BaseRegistry


class LLMRegistry(BaseRegistry):
    def get_item_name(self, llm):
        print("llm:", llm)
        return llm.model_name

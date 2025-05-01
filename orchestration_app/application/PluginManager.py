from domain.registry.BaseRegistry import BaseRegistry
from types import ModuleType


class PluginManager:
    def __init__(self, registrys: dict[str, BaseRegistry]):
        self.registrys = registrys

    async def register(
        self,
        category: str,
        module: ModuleType,
    ) -> None:
        registry = self.registrys.get(category)
        if not registry:
            raise ValueError(f"Registry for category {category} not found")
        if not hasattr(module, "register"):
            raise ValueError(f"Module does not have a register method")
        await module.register(registry)

    async def unregister(
        self,
        category: str,
        module_name: str,
    ) -> None:

        registry = self.registrys.get(category)
        if not registry:
            raise ValueError(f"Registry for category {category} not found")

        await registry.unregister(module_name)

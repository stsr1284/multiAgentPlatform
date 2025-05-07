from domain.registry.base_registry import BaseRegistry
from pathlib import Path
import importlib.util


class PluginManager:
    def __init__(self, registrys: dict[str, BaseRegistry]):
        self.registrys = registrys

    async def register(self, path: Path) -> None:
        category = path.parts[-2]
        module_name = path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            raise ValueError(f"Failed to load module {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        registry = self.registrys.get(category)
        if not registry:
            raise ValueError(f"Registry for category {category} not found")
        if not hasattr(module, "register"):
            raise ValueError(f"Module does not have a register method")
        await module.register(registry)

    async def unregister(
        self,
        path: Path,
    ) -> None:
        category = path.parts[-2]
        module_name = path.stem
        registry = self.registrys.get(category)
        if not registry:
            raise ValueError(f"Registry for category {category} not found")

        await registry.unregister(module_name)

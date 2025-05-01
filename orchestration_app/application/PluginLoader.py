from watchfiles import awatch, Change
from pathlib import Path
import importlib.util
from shared.loggin_config import logger


class AsyncPluginLoader:
    def __init__(self, plugin_base: str, registries: dict):
        self.plugin_base = Path(plugin_base).resolve()
        self.registries = registries

    async def load_module(self, file_path: Path, category: str):
        try:
            if not file_path.suffix == ".py" or file_path.name.startswith("__"):
                return

            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                return

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            registry = self.registries.get(category)
            if not registry:
                return
            if category == "tool" and hasattr(module, "register_tool"):
                await module.register_tool(registry)
            elif category == "llm" and hasattr(module, "register_llm"):
                await module.register_llm(registry)
            elif category == "builder" and hasattr(module, "register_builder"):
                await module.register_builder(registry)
            else:
                logger.warning(
                    f"[WARNING] No register function found for {category} in {module_name}"
                )
                return
            logger.info(
                f"[INFO] Loaded {category} module: {module_name} from {file_path}"
            )

        except Exception as e:
            logger.error(f"[ERROR] Failed to load {file_path}: {e}")

    async def setup(self):
        """
        런타임 시작 시 플러그인 디렉토리 내의 모든 플러그인을 탐색하고 초기 로딩합니다.
        """
        for category_dir in self.plugin_base.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name
            for file_path in category_dir.glob("*.py"):
                if file_path.name.startswith("__"):
                    continue
                await self.load_module(file_path, category)

    async def watch(self):
        async for changes in awatch(self.plugin_base):
            for change, path_str in changes:
                path = Path(path_str).resolve()
                if not path.is_file() and change != Change.deleted:
                    continue

                try:
                    rel_path = path.relative_to(self.plugin_base.resolve())
                except ValueError:
                    logger.warning(
                        f"[WARNING] {path} is not inside {self.plugin_base}. Skipping."
                    )
                    continue

                category = rel_path.parts[0]
                module_name = path.stem

                if change == 3:
                    registry = self.registries.get(category)
                    if not registry:
                        continue

                    try:
                        if category == "tool" and hasattr(registry, "unregister"):
                            await registry.unregister(module_name)
                        elif category == "llm" and hasattr(registry, "unregister"):
                            await registry.unregister(module_name)
                        elif category == "builder" and hasattr(registry, "unregister"):
                            await registry.unregister(module_name)
                    except Exception as e:
                        logger.error(
                            f"[ERROR] Failed to unregister {module_name} from {category} registry: {e}"
                        )
                        continue

                    logger.info(
                        f"[INFO] Unregistering {module_name} from {category} registry due to file deletion"
                    )
                else:
                    await self.load_module(path, category)

    async def watcher
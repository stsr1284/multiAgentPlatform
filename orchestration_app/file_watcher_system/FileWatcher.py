from domain.interfaces.FileWatcherInterface import FileWatcherInterface
from shared.loggin_config import logger
from typing import Callable, Awaitable
from watchfiles import awatch, Change
from pathlib import Path
import asyncio


class FileWatcher(FileWatcherInterface):
    def __init__(self, watch_path: str):
        self.watch_path = Path(watch_path).resolve()
        self.handlers: list[Callable[[Change, Path], Awaitable[None]]] = []
        self._stop_event = asyncio.Event()

    def register_handler(self, handler: Callable[[Change, Path], Awaitable[None]]):
        self.handlers.append(handler)

    async def watch(self):
        async for changes in awatch(self.watch_path):
            if self._stop_event.is_set():
                break
            for change, path_str in changes:
                path = Path(path_str).resolve()
                for handler in self.handlers:
                    if not callable(handler):
                        logger.warning(f"Handler {handler} is not callable")
                        continue
                    try:
                        await handler(change, path)
                    except Exception as e:
                        logger.error(f"Error in handler {handler}: {e}")

    async def stop(self):
        self._stop_event.set()


# class PluginLoader:
#     def __init__(self, plugin_base: str, plugin_manager: PluginManager):
#         self.plugin_base = Path(plugin_base).resolve()
#         self.plugin_manager = plugin_manager

#     async def setup(self):
#         for category_dir in self.plugin_base.iterdir():
#             if not category_dir.is_dir():
#                 continue

#             category = category_dir.name
#             for path in category_dir.glob("*.py"):
#                 if path.name.startswith("__"):
#                     continue
#                 spec = importlib.util.spec_from_file_location(path.stem, path)
#                 if not spec or not spec.loader:
#                     continue
#                 try:
#                     module = importlib.util.module_from_spec(spec)
#                     spec.loader.exec_module(module)

#                     await self.plugin_manager.register(category, module)
#                 except Exception as e:
#                     logger.error(f"Failed to load module {path}: {e}")
#                     continue

# async def setup(self):
#     for category_dir in self.plugin_base.iterdir():
#         if not category_dir.is_dir():
#             continue

#         category = category_dir.name
#         for path in category_dir.glob("*.py"):
#             if path.name.startswith("__"):
#                 continue
#             spec = importlib.util.spec_from_file_location(path.stem, path)
#             if not spec or not spec.loader:
#                 continue
#             try:
#                 module = importlib.util.module_from_spec(spec)
#                 spec.loader.exec_module(module)

#                 await self.plugin_manager.register(category, module)
#             except Exception as e:
#                 logger.error(f"Failed to load module {path}: {e}")
#                 continue

# async def watch(self):
#     async for changes in awatch(self.plugin_base):
#         for change, path_str in changes:
#             path = Path(path_str).resolve()
#             if not path.suffix == ".py" or path.name.startswith("__"):
#                 continue
#             try:
#                 rel_path = path.relative_to(self.plugin_base.resolve())
#             except ValueError:
#                 logger.warning(
#                     f"Path {path} is not a subdirectory of {self.plugin_base}"
#                 )
#                 continue
#             category = rel_path.parts[0]
#             module_name = path.stem

#             if change == Change.deleted:
#                 print(f"File deleted: {path}")
#                 try:
#                     await self.plugin_manager.unregister(category, module_name)
#                 except ValueError:
#                     logger.warning(
#                         f"Failed to unregister {module_name} from {category}"
#                     )
#                     continue
#             elif path.is_file():
#                 try:
#                     spec = importlib.util.spec_from_file_location(module_name, path)
#                     if not spec or not spec.loader:
#                         continue

#                     module = importlib.util.module_from_spec(spec)
#                     spec.loader.exec_module(module)
#                     print(f"File modified: {path}")
#                     await self.plugin_manager.register(category, module)
#                 except Exception as e:
#                     logger.error(f"Failed to load module {module_name}: {e}")
#                     continue

# async def _load_all_from_category(self, category_dir: Path):
#     category = category_dir.name
#     for path in category_dir.glob("*.py"):
#         if path.name.startswith("__"):
#             continue

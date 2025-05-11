from domain.system_setup.plugin_manager import PluginManager
from watchfiles import Change
from pathlib import Path


def create_plugin_handler(plugin_manager: PluginManager):
    async def handler(change: Change, path: Path):
        if path.suffix != ".py" or "plugin" not in path.parts:
            return

        try:
            if change in (Change.added, Change.modified):
                await plugin_manager.register(path=path)
            elif change == Change.deleted:
                await plugin_manager.unregister(path=path)
        except Exception as e:
            raise ValueError(f"Error create_plugin_handler '{path}': {e}") from e

    return handler

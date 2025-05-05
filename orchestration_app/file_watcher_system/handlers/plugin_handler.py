# plugin_system/handlers/plugin_handler.py
from watchfiles import Change
from pathlib import Path
from application.PluginManager import PluginManager


def create_plugin_handler(plugin_manager: PluginManager):
    async def handler(change: Change, path: Path):
        if path.suffix != ".py" or "plugin" not in path.parts:
            return

        if change in (Change.added, Change.modified):
            await plugin_manager.register(path=path)
        elif change == Change.deleted:
            await plugin_manager.unregister(path=path)

    return handler

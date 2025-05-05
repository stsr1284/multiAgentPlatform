# plugin_system/handlers/config_handler.py
from watchfiles import Change
from pathlib import Path
from application.AgentFactory import AgentFactory
import json


def create_config_handler(agent_factory: AgentFactory):
    async def handler(change: Change, path: Path):
        if path.name != "agent_config.json":
            return

        if change in (Change.added, Change.modified):
            try:
                config_data = json.loads(path.read_text())
                await agent_factory.create_agents_from_json(config_data)
            except Exception as e:
                print(f"[config_handler] Failed to reload config: {e}")

    return handler

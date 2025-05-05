from watchfiles import Change
from pathlib import Path

from application.OrchestratorBuilder import OrchestratorBuilder
import json


def create_orchestrator_config(orchestrator_builder: OrchestratorBuilder):
    async def handler(change: Change, path: Path):
        if path.name != "orchestrator_config.json":
            return

        if change in (Change.added, Change.modified):
            try:
                config_data = json.loads(path.read_text())
                await orchestrator_builder.create_orchestrators_from_json(config_data)
            except Exception as e:
                print(f"[config_handler] Failed to reload config: {e}")

    return handler

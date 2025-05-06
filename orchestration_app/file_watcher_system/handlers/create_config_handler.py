from domain.builder.base_builder import BaseBuilder
from watchfiles import Change
from pathlib import Path
import json


def create_config_handler(builder: BaseBuilder, target: str):
    async def handler(change: Change, path: Path):
        if path.name != target:
            return

        if change in (Change.added, Change.modified):
            try:
                config_data = json.loads(path.read_text())
                await builder.build_from_json(config_data)
            except Exception as e:
                raise ValueError(f"Error create_config_handler '{path}': {e}") from e

    return handler

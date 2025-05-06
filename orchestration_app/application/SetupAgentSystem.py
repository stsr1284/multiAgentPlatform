from domain.interfaces.SetupAgentSystemInterface import SetupAgentSystemInterface
from domain.builder.orchestrator_builder import OrchestratorBuilder
from domain.builder.agent_builder import AgentBuilder
from application.PluginManager import PluginManager
from shared.loggin_config import logger
from typing import Optional
from pathlib import Path
import asyncio
import json


class SetupAgentSystem(SetupAgentSystemInterface):
    def __init__(
        self,
        base_path: str,
        plugin_manager: PluginManager,
        agent_builder: AgentBuilder,
        orchestrator_builder: OrchestratorBuilder,
        config_path: Optional[str] = None,
        orchestrator_config: Optional[str] = None,
    ):
        self.base_path = Path(base_path).resolve()
        self.plugin_manager = plugin_manager
        self.agent_builder = agent_builder
        self.orchestrator_builder = orchestrator_builder
        self.config_path = (
            Path(config_path).resolve()
            if config_path
            else (self.base_path / "agent_config.json").resolve()
        )
        self.orchestrator_config = (
            Path(orchestrator_config).resolve()
            if orchestrator_config
            else (self.base_path / "orchestrator_config.json").resolve()
        )

    async def setup_agent_system(self):
        if not self.base_path.exists() or not self.base_path.is_dir():
            logger.warning(
                f"[Setup] Base path '{self.base_path}' does not exist or is not a directory."
            )
            return
        await self._load_plugins()
        await self._load_config()
        await self._load_orchestrator_config()

    async def _load_plugins(self):
        """디렉토리 내 플러그인을 비동기적으로 로딩합니다."""
        plugin_tasks = []

        for entry in self.base_path.iterdir():
            if entry.is_dir():
                plugin_tasks.extend(self._gather_plugin_tasks_from_dir(entry))

        if plugin_tasks:
            logger.info(f"[Setup] Registering {len(plugin_tasks)} plugin(s)...")
            await asyncio.gather(*plugin_tasks)
        else:
            logger.info("[Setup] No plugins found for registration.")

    async def _load_config(self):
        """설정 파일을 로딩합니다. (플러그인 등록 이후 호출되어야 함)"""
        if not self.config_path.exists() or not self.config_path.is_file():
            logger.warning(f"[Setup] Config file not found: {self.config_path}")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                await self.agent_builder.build_from_json(config_data)

        except Exception as e:
            logger.error(f"[Setup] Failed to load config file {self.config_path}: {e}")

    async def _load_orchestrator_config(self):
        if not self.config_path.exists() or not self.config_path.is_file():
            logger.warning(f"[Setup] Config file not found: {self.config_path}")
            return
        try:
            with open(self.orchestrator_config, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                await self.orchestrator_builder.build_from_json(config_data)
        except Exception as e:
            logger.error(
                f"[Setup] Failed to load orchestrator config file {self.orchestrator_config}: {e}"
            )

    def _gather_plugin_tasks_from_dir(self, directory: Path) -> list:
        tasks = []
        for file_path in directory.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            tasks.append(self._register_plugin(file_path.resolve()))
        return tasks

    async def _register_plugin(self, plugin_path: Path):
        try:
            await self.plugin_manager.register(plugin_path)
            logger.info(f"[Setup] Successfully registered plugin: {plugin_path}")
        except Exception as e:
            logger.error(f"[Setup] Failed to register plugin {plugin_path}: {e}")

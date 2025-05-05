from file_watcher_system.handlers.agent_config_handler import create_config_handler
from file_watcher_system.handlers.plugin_handler import create_plugin_handler
from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from application.InitializeService import InitializeService
from application.SetupAgentSystem import SetupAgentSystem
from file_watcher_system.FileWatcher import FileWatcher
from domain.registry.AgentRegistry import AgentRegistry
from domain.registry.ToolRegistry import ToolRegistry
from domain.registry.LLMRegistry import LLMRegistry
from application.PluginManager import PluginManager
from application.AgentFactory import AgentFactory

tool_registry = ToolRegistry()
llm_registry = LLMRegistry()
agent_builder_registry = AgentBuilderRegistry()
agent_registry = AgentRegistry()

agent_factory = AgentFactory(
    agentBuilderRegistry=agent_builder_registry,
    llmRegistry=llm_registry,
    toolRegistry=tool_registry,
    agentRegistry=agent_registry,
)

plugin_manager = PluginManager(
    registrys={
        "tool": tool_registry,
        "llm": llm_registry,
        "builder": agent_builder_registry,
    }
)

watcher = FileWatcher("plugin")
watcher.register_handler(create_plugin_handler(plugin_manager))
watcher.register_handler(create_config_handler(agent_factory))

setup_agent_system = SetupAgentSystem(
    base_path="plugin",
    plugin_manager=plugin_manager,
    agent_factory=agent_factory,
)

initialize_service = InitializeService(
    file_watcher=watcher,
    setup_agent_system=setup_agent_system,
)

__all__ = [
    "tool_registry",
    "llm_registry",
    "agent_builder_registry",
    "agent_registry",
    "agent_factory",
    "watcher",
    "initialize_service",
]

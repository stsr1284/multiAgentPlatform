from file_watcher_system.handlers.orchestrator_config_handler import (
    create_orchestrator_config,
)
from file_watcher_system.handlers.agent_config_handler import create_config_handler
from file_watcher_system.handlers.plugin_handler import create_plugin_handler
from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from domain.registry.OrchestratorRegistry import OrchestratorRegistry
from application.OrchestratorBuilder import OrchestratorBuilder
from application.InitializeService import InitializeService
from application.SetupAgentSystem import SetupAgentSystem
from domain.registry.AgentRegistry import AgentRegistry
from file_watcher_system.FileWatcher import FileWatcher
from domain.registry.GraphRegistry import GraphRegistry
from domain.registry.ToolRegistry import ToolRegistry
from application.resume_service import ResumeService
from domain.registry.LLMRegistry import LLMRegistry
from application.PluginManager import PluginManager
from application.AgentFactory import AgentFactory

from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import ResumeAStreamStrategy
from application.orchestration_service import OrchestrationService


tool_registry = ToolRegistry()
llm_registry = LLMRegistry()
agent_builder_registry = AgentBuilderRegistry()
agent_registry = AgentRegistry()
graph_registry = GraphRegistry()

agent_factory = AgentFactory(
    agentBuilderRegistry=agent_builder_registry,
    llmRegistry=llm_registry,
    toolRegistry=tool_registry,
    agentRegistry=agent_registry,
)

orchestrator_registry = OrchestratorRegistry()
orchestrator_builder = OrchestratorBuilder(
    agentBuilderRegistry=agent_builder_registry,
    llmRegistry=llm_registry,
    toolRegistry=tool_registry,
    orchestratorRegistry=orchestrator_registry,
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
watcher.register_handler(create_orchestrator_config(orchestrator_builder))

setup_agent_system = SetupAgentSystem(
    base_path="plugin",
    plugin_manager=plugin_manager,
    agent_factory=agent_factory,
    orchestrator_builder=orchestrator_builder,
)

initialize_service = InitializeService(
    file_watcher=watcher,
    setup_agent_system=setup_agent_system,
)

orchestration_astream_strategy = OrchestrationAStreamStrategy(
    graph_registry=graph_registry,
)
resume_astream_strategy = ResumeAStreamStrategy(graph_registry=graph_registry)

orchestration_service = OrchestrationService(
    agent_registry=agent_registry,
    orchestrator_registry=orchestrator_registry,
    graph_registry=graph_registry,
)

resume_service = ResumeService(graph_registry=graph_registry)


__all__ = [
    "tool_registry",
    "llm_registry",
    "agent_builder_registry",
    "agent_registry",
    "agent_factory",
    "watcher",
    "initialize_service",
    "orchestrator_registry",
    "graph_registry",
    "resume_service",
]

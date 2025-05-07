from domain.execution_strategies.orchestration_astream_strategy import (
    OrchestrationAStreamStrategy,
)
from domain.execution_strategies.resome_astream_strategy import ResumeAStreamStrategy
from file_watcher_system.handlers.create_config_handler import create_config_handler
from file_watcher_system.handlers.plugin_handler import create_plugin_handler
from domain.registry.agent_builder_registry import AgentBuilderRegistry
from domain.registry.orchestrator_registry import OrchestratorRegistry
from domain.builder.orchestrator_builder import OrchestratorBuilder
from application.orchestration_service import OrchestrationService
from application.InitializeService import InitializeService
from application.setup_agent_system import SetupAgentSystem
from domain.registry.agent_registry import AgentRegistry
from file_watcher_system.file_watcher import FileWatcher
from domain.registry.graph_registry import GraphRegistry
from domain.registry.tool_registry import ToolRegistry
from domain.builder.agent_builder import AgentBuilder
from application.resume_service import ResumeService
from domain.registry.llm_registry import LLMRegistry
from application.plugin_manager import PluginManager


llm_registry = LLMRegistry()
tool_registry = ToolRegistry()
agent_builder_registry = AgentBuilderRegistry()
agent_registry = AgentRegistry()
graph_registry = GraphRegistry()

agent_builder = AgentBuilder(
    agent_builder_registry=agent_builder_registry,
    llm_registry=llm_registry,
    tool_registry=tool_registry,
    agent_registry=agent_registry,
)

orchestrator_registry = OrchestratorRegistry()
orchestrator_builder = OrchestratorBuilder(
    agent_builder_registry=agent_builder_registry,
    llm_registry=llm_registry,
    tool_registry=tool_registry,
    orchestrator_registry=orchestrator_registry,
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
watcher.register_handler(create_config_handler(agent_builder, "agent_config.json"))
watcher.register_handler(
    create_config_handler(orchestrator_builder, "orchestrator_config.json")
)

setup_agent_system = SetupAgentSystem(
    base_path="plugin",
    plugin_manager=plugin_manager,
    agent_builder=agent_builder,
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
    "initialize_service",
    "llm_registry",
    "tool_registry",
    "agent_builder_registry",
    "agent_registry",
    "orchestrator_registry",
    "graph_registry",
    "orchestration_astream_strategy",
    "resume_astream_strategy",
    "orchestration_service",
    "resume_service",
]

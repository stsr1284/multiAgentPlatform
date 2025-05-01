from domain.registry.ToolRegistry import ToolRegistry
from domain.registry.LLMRegistry import LLMRegistry
from domain.registry.AgentBuilderRegistry import AgentBuilderRegistry
from application.AgentFactory import AgentFactory
from utils.config import settings
from langchain_openai import ChatOpenAI
from application.PluginLoader import AsyncPluginLoader

tool_registry = ToolRegistry()
llm_registry = LLMRegistry()
agent_builder_registry = AgentBuilderRegistry()

agent_factory = AgentFactory(agent_builder_registry, llm_registry, tool_registry)

plugin_loader = AsyncPluginLoader(
    plugin_base="plugin",
    registries={
        "tool": tool_registry,
        "llm": llm_registry,
        "builder": agent_builder_registry,
    },
)

# 이 container 객체들을 전역으로 공유할 수 있도록 export
__all__ = [
    "tool_registry",
    "llm_registry",
    "agent_builder_registry",
    "agent_factory",
    "plugin_loader",
]

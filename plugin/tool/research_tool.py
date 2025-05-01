from langchain.tools import tool


@tool
def research_tool(topic: str) -> str:
    """A simple research tool that takes a topic and returns a research statement."""
    if not isinstance(topic, str):
        raise ValueError("Topic must be a string.")
    if not topic:
        raise ValueError("Topic cannot be empty.")
    return f"Researching the topic: {topic}"


async def register(registry):
    await registry.register(research_tool)

from langchain.tools import tool
from langgraph.types import interrupt


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""

    return a + b


async def register(registry):
    await registry.register(add)

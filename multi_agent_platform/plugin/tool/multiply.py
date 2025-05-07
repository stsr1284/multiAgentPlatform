from langchain.tools import tool


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


async def register(registry):
    await registry.register(multiply)
